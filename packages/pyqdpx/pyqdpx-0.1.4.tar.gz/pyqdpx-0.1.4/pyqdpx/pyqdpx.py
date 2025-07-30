from __future__ import annotations  # For Python 3.7 compatibility with type hints
import zipfile
import re
import uuid
import os
from bs4 import BeautifulSoup, Tag
from datetime import datetime, timezone
import regex

# Define the GUID regex pattern for validation
GUID_PATTERN = re.compile(
    r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')

def simulate_nvivo_offsets(text):
    result = ""
    for g in regex.findall(r'\X', text):
        result += g
        for c in g:
            if ord(c) > 0xFFFF: # Add a zero-width space to simulate 2-char width
                result += "\u200B"
    return result

class User:
    """
    Represents a user within the QDE project,
    containing their GUID, ID, and name.
    """
    def __init__(self, name: str, id: str = None, guid: str = None):
        """
        Initializes a User object.

        Args:
            name (str):
                The full name of the user (e.g., "John Doe").
            id (str, optional):
                The short identifier for the user (e.g., "JD").
            guid (str, optional):
                The unique identifier (GUID) for the user.
                If provided, it must conform to the standard
                UUID format. If not provided, a new, valid
                GUID will be generated.

        Raises:
            ValueError:
                If a GUID is provided but does not match the expected
                UUID pattern.
        """
        self.id = id
        self.name = name
        if guid:
            # Validate the provided GUID against the regex pattern
            if not GUID_PATTERN.match(guid):
                raise ValueError(f"Invalid GUID format: '{guid}'. "
                                 f"Expected format: {GUID_PATTERN.pattern}")
            self.guid = guid
        else:
            # Generate a new random GUID if none is provided
            self.guid = str(uuid.uuid4())

    def __repr__(self):
        """
        Provides a developer-friendly string representation of the User object.
        """
        self_id_str = f"'{self.id}'" if self.id else "None"
        return f"User(guid='{self.guid}', name='{self.name}', id={self_id_str})"

    def __eq__(self, other):
        """
        Compares two User objects for equality based on their GUID, ID, and name.
        """
        if not isinstance(other, User):
            return NotImplemented
        return self.guid == other.guid and self.id == other.id and self.name == other.name

class Code:
    """
    Represents a qualitative code within the QDE project's CodeBook.
    Codes can form a hierarchical tree structure.
    """
    def __init__(self, name: str, qde_instance, guid: str = None,
                 is_codable: bool = True, parent=None, description: str = None,
                 _xml_tag: Tag = None):
        """
        Initializes a Code object.

        Args:
            name (str):
                The name of the code.
            qde_instance (QDE):
                A reference to the parent QDE object, necessary
                to access the BeautifulSoup object and modified flag.
            guid (str, optional):
                The unique identifier (GUID) for the code.
                If None, a new GUID is generated.
            is_codable (bool, optional):
                Whether the code can be applied to data. Defaults to True.
            parent (Code, optional):
                The parent Code object in the hierarchy.
                None if it's a top-level code.
            description (str, optional):
                A descriptive text for the code.
            _xml_tag (bs4.Tag, optional):
                Internal use. The BeautifulSoup Tag corresponding to this code
                if it's being loaded from existing XML.
        """
        self._qde_instance = qde_instance
        self._xml_tag = _xml_tag # The BeautifulSoup Tag for this code

        self.name_val = name # Use internal variables to avoid triggering setters during init
        self.is_codable_val = is_codable
        self.description_val = description

        if guid:
            if not GUID_PATTERN.match(guid):
                raise ValueError(f"Invalid GUID format: '{guid}'. "
                                 f"Expected pattern: {GUID_PATTERN.pattern}")
            self.guid = guid
        else:
            self.guid = str(uuid.uuid4())

        self._parent_guid: str | None = None # GUID of the parent
        if parent:
            self._parent_guid = parent.guid

        self._children_guids: list[str] = [] # List of GUIDs of child codes

        # Add this code to the QDE's _codes dict
        # This needs to happen before children can reference it as a parent
        self._qde_instance._codes[self.guid] = self

        # If a parent is provided, add this code's GUID to the parent's children list
        if parent:
            parent._children_guids.append(self.guid)

        # If the QDE's _codes dict has already been initialized from XML
        # and this code is newly created (not loaded from XML),
        # then add it to the BeautifulSoup object
        if self._qde_instance._codes_initialized_from_xml and not _xml_tag:
            self._add_to_bs4()
            self._qde_instance.modified = True

    def _add_to_bs4(self):
        """
        Adds this new Code object as an XML Tag to the QDE's BeautifulSoup object.
        This is called only when a new Code object is programmatically created
        after the initial XML loading.
        """
        new_code_tag = self._qde_instance._bs4_obj.new_tag('Code')
        new_code_tag['guid'] = self.guid
        new_code_tag['name'] = self.name_val
        new_code_tag['isCodable'] = str(self.is_codable_val).lower() # XML expects "true"/"false"

        if self.description_val:
            desc_tag = self._qde_instance._bs4_obj.new_tag('Description')
            desc_tag.string = self.description_val
            new_code_tag.append(desc_tag)

        parent_xml_tag = None
        if self._parent_guid:
            # Find the parent's XML tag by its GUID
            parent_code_obj = self._qde_instance._codes.get(self._parent_guid)
            if parent_code_obj and parent_code_obj._xml_tag:
                parent_xml_tag = parent_code_obj._xml_tag
        else:
            # If no parent, find the <Codes> tag
            codebook_tag = self._qde_instance._bs4_obj.find('CodeBook')
            if codebook_tag:
                parent_xml_tag = codebook_tag.find('Codes')

        if parent_xml_tag:
            parent_xml_tag.append(new_code_tag)
            self._xml_tag = new_code_tag # Assign the newly created XML tag
        else:
            print("Warning: Could not find parent XML tag for code "
                  f"'{self.name_val}' ({self.guid}). Not added to BS4.")

    @property
    def name(self) -> str:
        """Getter for the code's name."""
        return self.name_val

    @name.setter
    def name(self, new_name: str):
        """Setter for the code's name."""
        if self.name_val != new_name:
            self.name_val = new_name
            if self._xml_tag:
                self._xml_tag['name'] = new_name
                self._qde_instance.modified = True

    @property
    def description(self) -> str | None:
        """Getter for the code's description."""
        return self.description_val

    @description.setter
    def description(self, new_description: str | None):
        """Setter for the code's description."""
        if self.description_val != new_description:
            self.description_val = new_description
            if self._xml_tag:
                desc_tag = self._xml_tag.find('Description')
                if new_description:
                    if desc_tag:
                        desc_tag.string = new_description
                    else:
                        # Create new Description tag if it doesn't exist
                        new_desc_tag = self._qde_instance._bs4_obj.new_tag('Description')
                        new_desc_tag.string = new_description
                        self._xml_tag.insert(0, new_desc_tag) # Insert as first child
                else: # new_description is None, remove existing description
                    if desc_tag:
                        desc_tag.decompose() # Remove the tag from the XML
                self._qde_instance.modified = True

    @property
    def is_codable(self) -> bool:
        """Getter for the code's is_codable status."""
        return self.is_codable_val

    @is_codable.setter
    def is_codable(self, value: bool):
        """Setter for the code's is_codable status."""
        if self.is_codable_val != value:
            self.is_codable_val = value
            if self._xml_tag:
                self._xml_tag['isCodable'] = str(value).lower()
                self._qde_instance.modified = True

    @property
    def children(self) -> list[Code]:
        """
        Getter for the list of child Code objects.
        """
        return [self._qde_instance._codes[guid]
                for guid in self._children_guids
                if guid in self._qde_instance._codes]

    @property
    def parent(self) -> Code | None:
        """
        Getter for the parent Code object.
        Returns None if it's a top-level code.
        """
        if (self._parent_guid
            and self._parent_guid in self._qde_instance._codes):
            return self._qde_instance._codes[self._parent_guid]
        return None

    def delete(self):
        """
        Deletes this code from the codebook.
        Raises an exception if the code has children.
        """
        if self._children_guids:
            raise Exception(f"Cannot delete code '{self.name_val}' ({self.guid}) "
                            "because it has children. Delete children first.")

        for source in self._qde_instance.sources.values():
            if source.find_code_selections(self):
                raise RuntimeError(
                    f"Cannot delete code '{self.name_val}' ({self.guid}) " 
                    f"because it has been used to annotate selections in "
                    f"source {source.name}. Remove selections first.")

        # Remove from QDE's _codes dict
        if self.guid in self._qde_instance._codes:
            del self._qde_instance._codes[self.guid]

        # Remove from parent's children list (if it has a parent)
        parent_obj = self.parent
        if parent_obj:
            if self.guid in parent_obj._children_guids:
                parent_obj._children_guids.remove(self.guid)

        # Remove the XML tag from the BeautifulSoup object
        if self._xml_tag:
            self._xml_tag.decompose() # This removes the tag from the XML tree

        self._qde_instance.modified = True
        print(f"Code '{self.name_val}' ({self.guid}) successfully deleted.")


    def __repr__(self):
        """
        Provides a developer-friendly string
        representation of the Code object.
        """
        self_parent_guid_str =\
            f"'{self._parent_guid}'" if self._parent_guid else "None"
        return (f"Code(guid='{self.guid}', name='{self.name_val}', "
                f"is_codable={self.is_codable_val}, "
                f"parent_guid={self_parent_guid_str}, "
                f"children_count={len(self._children_guids)})")


class Source:
    """
    Represents a text source within the QDE project,
    corresponding to a TextSource XML element.
    It manages the source's metadata, content,
    and associated coded selections.
    """
    class Selection:
        """
        Represents a PlainTextSelection XML element within a Source,
        linking a span of text to a code.
        """
        def __init__(self, source_instance: Source, start: int, end: int,
                     code: Code, user: User, description: str = None, 
                     guid: str = None, _xml_tag: Tag = None):
            """
            Initializes a Selection object.

            Args:
                source_instance (Source):
                    The parent Source object this selection belongs to.
                start (int):
                    The starting character position of the
                    selection in the plain text.
                end (int):
                    The ending character position of the
                    selection in the plain text.
                code (Code):
                    The Code object applied to this selection.
                user (User):
                    The User object who created this selection.
                description (str, optional):
                    A description for the selection.
                guid (str, optional):
                    The GUID of the PlainTextSelection.
                    If None, a new one is generated.
                _xml_tag (bs4.Tag, optional):
                    Internal use. The BeautifulSoup Tag corresponding
                    to this selection if it's being loaded from existing XML.
            """
            self._source_instance = source_instance
            self._qde_instance = source_instance._qde_instance
            self._xml_tag = _xml_tag
            self._code_obj = code
            self._user_obj = user

            self.start_position = start
            self.end_position = end
            self.description = description

            if guid:
                if not GUID_PATTERN.match(guid):
                    raise ValueError("Invalid GUID format for Selection: "
                                     f"'{guid}'. Expected pattern: " 
                                     + GUID_PATTERN.pattern)
                self.guid = guid
            else:
                self.guid = str(uuid.uuid4())

            # If this is a newly created selection (not loaded from XML), add to BS4
            if not _xml_tag:
                self._add_to_bs4()
                self._qde_instance.modified = True
                self._source_instance.coded_selections[self.guid] = self # Add to parent's dict
        
        # start and end properties
        @property
        def start(self) -> int:
            """Getter for the start position of the selection."""
            return self.start_position
        @start.setter
        def start(self, new_start: int):
            """Setter for the start position of the selection."""
            if new_start < 0 or new_start >= self.end_position:
                raise ValueError(f"Invalid start position: {new_start}. "
                                 "Must be >= 0 and < end position "
                                 f"({self.end_position}).")
            self.start_position = new_start
            if self._xml_tag:
                self._xml_tag['startPosition'] = str(new_start)
                self._qde_instance.modified = True

        @property
        def end(self) -> int:
            """Getter for the end position of the selection."""
            return self.end_position
        @end.setter
        def end(self, new_end: int):
            """Setter for the end position of the selection."""
            if (new_end <= self.start_position
                or new_end > len(self._source_instance.text_content)):
                raise ValueError(
                    f"Invalid end position: {new_end}. Must be > "
                    f"start position ({self.start_position}) and "
                    f"<= text length ({len(self._source_instance.text_content)}).")
            self.end_position = new_end
            if self._xml_tag:
                self._xml_tag['endPosition'] = str(new_end)
                self._qde_instance.modified = True

        def _add_to_bs4(self):
            """
            Adds this new Selection object as an XML Tag to the parent Source's
            BeautifulSoup object.
            """
            # Create PlainTextSelection tag
            selection_tag =\
                self._qde_instance._bs4_obj.new_tag('PlainTextSelection')
            selection_tag['guid'] = self.guid
            selection_tag['name'] = "" # As per schema, name is empty
            selection_tag['startPosition'] = str(self.start_position)
            selection_tag['endPosition'] = str(self.end_position)
            selection_tag['creatingUser'] = self._user_obj.guid
            selection_tag['creationDateTime'] =\
                datetime.now().isoformat(timespec='seconds') + 'Z'
            selection_tag['modifyingUser'] = self._user_obj.guid
            selection_tag['modifiedDateTime'] =\
                datetime.now().isoformat(timespec='seconds') + 'Z'

            # Add Description child (empty)
            desc_tag = self._qde_instance._bs4_obj.new_tag('Description')
            desc_tag.string = self.description if self.description else ""
            selection_tag.append(desc_tag)

            # Add Coding child
            coding_tag = self._qde_instance._bs4_obj.new_tag('Coding')
            coding_tag['guid'] = str(uuid.uuid4()) # Coding has its own random GUID
            coding_tag['creatingUser'] = self._user_obj.guid
            coding_tag['creationDateTime'] =\
                datetime.now().isoformat(timespec='seconds') + 'Z'
            selection_tag.append(coding_tag)

            # Add CodeRef child
            code_ref_tag = self._qde_instance._bs4_obj.new_tag('CodeRef')
            code_ref_tag['targetGUID'] = self._code_obj.guid
            coding_tag.append(code_ref_tag)

            # Append the new selection tag to the parent TextSource XML tag
            if self._source_instance._xml_tag:
                self._source_instance._xml_tag.append(selection_tag)
                self._xml_tag = selection_tag # Assign the newly created XML tag
            else:
                print("Warning: Could not find parent TextSource "
                      "XML tag for selection. Not added to BS4.")

        @property
        def code(self) -> Code:
            """Getter for the Code object associated with this selection."""
            return self._code_obj

        @property
        def user(self) -> User:
            """Getter for the User object who created this selection."""
            return self._user_obj

        @property
        def text(self) -> str:
            """
            Returns the selected substring of the
            source's plain text content.
            """
            return self._source_instance.text_content[self.start_position:self.end_position]
        
        def delete(self):
            """
            Deletes this selection from its parent Source.
            """
            if self.guid in self._source_instance.coded_selections:
                del self._source_instance.coded_selections[self.guid]
            
            if self._xml_tag:
                self._xml_tag.decompose()
                self._qde_instance.modified = True
            print(f"Selection '{self.guid}' successfully deleted.")


        def __repr__(self):
            description = f"'self.description'" if self.description else None
            return (f"Selection(guid='{self.guid}', "
                    f"start={self.start_position}, "
                    f"end={self.end_position}, "
                    f"user='{self.user.name}, "
                    f"code='{self.code.name}', "
                    f"description='{description}', "
                    f"text='{self.text}')")


    def __init__(self, name: str, qde_instance: QDE, guid: str = None,
                 rich_text_path: str = None,
                 creating_user_guid: str = None, creation_date_time: str = None,
                 modifying_user_guid: str = None, modified_date_time: str = None,
                 _xml_tag: Tag = None):
        """
        Initializes a Source object.

        Args:
            name (str):
                The name of the source file (e.g., "videos_selection.docx").
            qde_instance (QDE):
                A reference to the parent QDE object.
            guid (str, optional):
                The unique identifier (GUID) for the source.
                If None, a new GUID is generated.
            rich_text_path (str, optional):
                The path to the rich text file
                (e.g., "internal://{guid}.docx").
            creating_user_guid (str, optional):
                GUID of the user who created the source.
            creation_date_time (str, optional):
                Timestamp of source creation.
            modifying_user_guid (str, optional):
                GUID of the user who last modified the source.
            modified_date_time (str, optional):
                Timestamp of last modification.
            _xml_tag (bs4.Tag, optional):
                Internal use. The BeautifulSoup Tag
                corresponding to this source if it's
                being loaded from existing XML.
        """
        self._qde_instance = qde_instance
        self._xml_tag = _xml_tag

        self.name = name
        
        if guid:
            if not GUID_PATTERN.match(guid):
                raise ValueError(f"Invalid GUID format for Source: '{guid}'. "
                                 f"Expected pattern: {GUID_PATTERN.pattern}")
            self.guid = guid
        else:
            self.guid = str(uuid.uuid4())

        self.plain_text_path = f"internal://{guid}.txt" if guid else None
        self.rich_text_path = rich_text_path
        self.creating_user_guid = creating_user_guid
        self.creation_date_time = creation_date_time
        self.modifying_user_guid = modifying_user_guid
        self.modified_date_time = modified_date_time

        self.text_content: str | None = None # Will be loaded by QDPX

        self.coded_selections: dict[str, Source.Selection] = {} # Stores Selection objects by their GUID

        # Populate coded_selections from XML if _xml_tag is provided
        if _xml_tag:
            self._parse_selections_from_xml()
        
        # Add this source to the QDE's _sources dict if it's new
        # This is handled by QDE's _parse_source_element and add_source methods

    def _parse_selections_from_xml(self):
        """
        Parses PlainTextSelection elements from the source's XML tag
        and populates the coded_selections dictionary.
        """
        if not self._xml_tag:
            return

        for selection_tag in self._xml_tag.find_all('PlainTextSelection',
                                                    recursive=False):
            guid = selection_tag.get('guid')
            start_pos = int(selection_tag.get('startPosition'))
            end_pos = int(selection_tag.get('endPosition'))
            creating_user_guid = selection_tag.get('creatingUser')

            coding_tag = selection_tag.find('Coding', recursive=False)
            if not coding_tag:
                print(f"Warning: Skipping selection {guid} in "
                      f"source {self.name}: Missing Coding tag.")
                continue
            
            code_ref_tag = coding_tag.find('CodeRef', recursive=False)
            if not code_ref_tag:
                print(f"Warning: Skipping selection {guid} in "
                      f"source {self.name}: Missing CodeRef tag.")
                continue

            target_code_guid = code_ref_tag.get('targetGUID')
            
            # Resolve Code and User objects
            code_obj = self._qde_instance.codes.get(target_code_guid)
            user_obj = self._qde_instance.users.get(creating_user_guid)

            if not code_obj:
                print(f"Warning: Skipping selection {guid} in "
                      f"source {self.name}: Code with "
                      f"GUID {target_code_guid} not found.")
                continue
            if not user_obj:
                print(f"Warning: Skipping selection {guid} in "
                      f"source {self.name}: User with "
                      f"GUID {creating_user_guid} not found.")
                continue

            try:
                selection = Source.Selection(
                    source_instance=self,
                    start=start_pos,
                    end=end_pos,
                    code=code_obj,
                    user=user_obj,
                    guid=guid,
                    _xml_tag=selection_tag
                )
                self.coded_selections[guid] = selection
            except ValueError as e:
                print(f"Error creating Selection object for "
                      "source {self.name}, guid {guid}: {e}")

    def add_selection(self, start: int, end: int,
                      code: Code, user: User,
                      description: str = None) -> Selection:
        """
        Adds a new PlainTextSelection to this source.

        Args:
            start (int):
                The starting character position of the selection.
            end (int):
                The ending character position of the selection.
            code (Code):
                The Code object to apply to this selection.
            user (User):
                The User object creating this selection.
            description (str, optional):
                A description for the selection.

        Returns:
            Source.Selection:
                The newly created Selection object.

        Raises:
            ValueError: If start/end positions are invalid or 
            out of bounds, or if the provided code is not codable.
        """
        if not (0 <= start < end <= len(self.text_content)):
            raise ValueError(
                f"Invalid selection range: start={start}, end={end}. "
                f"Text length: {len(self.text_content)}")
        if not isinstance(code, Code):
            raise TypeError(
                "Provided 'code' must be an instance of the Code class.")
        if not code.is_codable:
            raise ValueError(
                f"Cannot apply code '{code.name}' ({code.guid}) "
                "to selection because it is not codable.")
        if not isinstance(user, User):
            raise TypeError(
                "Provided 'user' must be an instance of the User class.")

        new_selection = Source.Selection(self, start, end, code, user,
                                         description=description)
        # The Selection's init handles adding itself to self.coded_selections and BS4
        return new_selection

    def find_user_selections(self, user: User) -> list[Selection]:
        """
        Finds all selections made by a specific user in this source.

        Args:
            user (User):
                The User object to search for.

        Returns:
            list[Source.Selection]:
                A list of Selection objects created by the specified user.
        """
        return [sel for sel in self.coded_selections.values()
                if sel.user == user]

    def find_code_selections(self, code: Code) -> list[Selection]:
        """
        Finds all selections coded with a specific code in this source.

        Args:
            code (Code):
                The Code object to search for.

        Returns:
            list[Source.Selection]:
                A list of Selection objects coded with the specified code.
        """
        return [sel for sel in self.coded_selections.values()
                if sel.code == code]

    def __repr__(self):
        return (f"Source(guid='{self.guid}', name='{self.name}', "
                f"plain_text_path='{self.plain_text_path}', "
                f"selections_count={len(self.coded_selections)})")


class QDE:
    """
    Represents the parsed content of a 'project.qde' XML file.
    It allows for accessing and modifying project-specific data,
    such as users, codes, and sources.
    """
    def __init__(self, xml_content: str, qdpx: QDPX):
        """
        Initializes the QDE object by parsing the XML content.

        Args:
            xml_content (str):
                The complete XML content of the 'project.qde' file
                as a string. This content is then parsed into a
                BeautifulSoup object for easy manipulation.
            qdpx (QDPX):
                The QDPX object that contains the path to the zip file
        """
        # Parse the XML content using BeautifulSoup, specifying 'xml' parser
        self._bs4_obj = BeautifulSoup(xml_content, 'xml')
        # Store a reference to the QDPX object for saving changes later
        self._qdpx = qdpx
        # A flag to indicate if any modifications have been made to the XML
        # content via this QDE object. This is crucial for determining
        # whether to save changes back to the QDPX file.
        self.modified = False
        # Populate the users dict
        self.users

        # Initialize code-related variables
        # self._codes: dict[str, Code] = {} # Stores all Code objects by GUID
        self._codes_initialized_from_xml = False # Flag to track if _codes has been populated from XML
        # Parse the codes from the XML if they exist
        self.codes  # Access the property to ensure codes are loaded

        # Initialize sources-related variables
        # self._sources: dict[str, Source] = {} # Stores all Source objects by GUID
        self._sources_initialized_from_xml = False
        self.sources # Access the property to ensure sources are loaded

    @property
    def users(self) -> dict[User]:
        """
        Retrieves, initializes and caches a dict of User objects by their GUID 
        from the parsed XML if not already done, then returns the dictionary.

        Returns:
            dict[User]: A dict containing User objects found in the XML.
                        Returns an empty dict if no <Users> section or no
                        <User> tags are present.
        """
        # if _users already exists, return it directly
        if hasattr(self, '_users'):
            return self._users
        
        self._users = {}

        # Find the <Users> tag in the XML document
        users_tag = self._bs4_obj.find('Users')
        if users_tag:
            # Iterate over all <User> tags found within the <Users> tag
            for user_tag in users_tag.find_all('User'):
                # Extract attributes from the <User> tag
                name = user_tag.get('name')
                guid = user_tag.get('guid')
                user_id = user_tag.get('id')  # This is optional, can be None

                # Only create a User object if all required attributes are present
                if guid and name:
                    try:
                        # Attempt to create a User object; handles GUID validation internally
                        self._users[guid] = User(guid=guid,
                                                 id=user_id,
                                                 name=name)
                    except ValueError as e:
                        # Log a warning if a user in the XML has an invalid GUID,
                        # but continue processing other users.
                        print("Warning: Skipping user with "
                              f"invalid GUID in XML: {guid} - {e}")
        return self._users

    def add_user(self, user: User):
        """
        Adds a new User object to the project's XML structure.
        This method will create or locate the <Users> element and then
        append a new <User> element with the provided user's data.

        Args:
            user (User): The User object to be added to the project.
        """
        # Find the existing <Users> tag or create a new one if it doesn't exist
        users_tag = self._bs4_obj.find('Users')
        if not users_tag:
            # If <Users> tag does not exist, find the root element of the XML
            # and append <Users> as its child. This assumes a single root element.
            root_tag = None
            if self._bs4_obj.contents:
                # Find the first actual tag among the document's contents
                for content in self._bs4_obj.contents:
                    if content.name: # Check if it's a tag (has a name)
                        root_tag = content
                        break
            
            if root_tag:
                # Create a new <Users> tag
                users_tag = self._bs4_obj.new_tag('Users')
                root_tag.append(users_tag) # Append it to the root
            else:
                print("Error: Could not find a suitable root "
                      "element in the XML to add <Users> section.")
                return # Cannot add user if no root element exists

        # Create a new <User> tag using the BeautifulSoup object's factory method
        user_tag = self._bs4_obj.new_tag('User')
        # Set the attributes for the new <User> tag from the User object
        user_tag['guid'] = user.guid
        if user.id:
            user_tag['id'] = user.id
        user_tag['name'] = user.name

        # Append the newly created <User> tag to the <Users> tag
        users_tag.append(user_tag)
        # Mark the QDE object as modified, indicating that changes need to be saved
        self.modified = True
        self._users[user.guid] = user  # Update the in-memory users dict

    @property
    def codes(self) -> dict[str, Code]:
        """
        Retrieves and initializes the codebook from the XML if not already done,
        then returns a dictionary of all Code objects by their GUID.
        """
        if not self._codes_initialized_from_xml:
            self._codes = {} # Clear any potential previous state
            codebook_tag = self._bs4_obj.find('CodeBook')
            if codebook_tag:
                codes_root_tag = codebook_tag.find('Codes')
                if codes_root_tag:
                    # Start recursive parsing from top-level codes
                    for code_xml_tag in codes_root_tag.find_all('Code', recursive=False):
                        self._parse_code_element(code_xml_tag,
                                                 parent_code_obj=None)
            self._codes_initialized_from_xml = True
        return self._codes

    def _parse_code_element(self, xml_tag: Tag,
                            parent_code_obj: Code = None):
        """
        Helper method to recursively parse
        <Code> XML elements and create Code objects.
        """
        guid = xml_tag.get('guid')
        name = xml_tag.get('name')
        is_codable_str = xml_tag.get('isCodable', 'true')
        is_codable = is_codable_str.lower() == 'true'

        description_tag = xml_tag.find('Description')
        description = (description_tag.string
                       if description_tag and description_tag.string
                       else None)

        if not guid or not name:
            print("Warning: Skipping malformed Code XML "
                  f"tag (missing guid or name): {xml_tag}")
            return

        try:
            # Create the Code object.
            # Pass self (QDE instance) and the XML tag.
            # _xml_tag is crucial for setters/deleters
            # to modify the correct XML element.
            code_obj = Code(name=name, guid=guid, is_codable=is_codable,
                            parent=parent_code_obj, description=description,
                            qde_instance=self, _xml_tag=xml_tag)

            # Recursively parse children
            for child_xml_tag in xml_tag.find_all('Code', recursive=False):
                self._parse_code_element(child_xml_tag,
                                         parent_code_obj=code_obj)
        except ValueError as e:
            print(f"Error creating Code object from "
                  f"XML for '{name}' ({guid}): {e}")

    def print_code_tree(self):
        """
        Prints the entire code tree with indentation and ASCII art.
        """
        print("\n--- Code Tree ---")
        if not self.codes: # Access the property to ensure it's loaded
            print("No codes found in the project.")
            return

        # Find top-level codes (those whose _parent_guid is None)
        # Filter self.codes to get only top-level codes based on their XML structure parent
        top_level_codes = []
        codebook_tag = self._bs4_obj.find('CodeBook')
        if codebook_tag:
            codes_root_tag = codebook_tag.find('Codes')
            if codes_root_tag:
                # Iterate through direct children of <Codes> to find actual top-level code XML tags
                for xml_tag in codes_root_tag.find_all('Code', recursive=False):
                    # Find the corresponding Code object from our loaded _codes dict
                    guid = xml_tag.get('guid')
                    if guid and guid in self._codes:
                        code_obj = self._codes[guid]
                        if not code_obj.parent: # Verify it's a top-level code object
                            top_level_codes.append(code_obj)
        
        # Sort top-level codes by name for consistent output
        top_level_codes.sort(key=lambda c: c.name)

        def _print_node(code_obj: Code, level: int, prefix: str):
            """Recursive helper for printing individual code nodes."""
            indent = "│    " * level
            display_name = f"'{code_obj.name}'"
            if code_obj.description:
                display_name += "*"
            
            print(f"{indent}{prefix}{display_name}")

            # Sort children by name for consistent output
            sorted_children = sorted(code_obj.children, key=lambda c: c.name)

            for i, child in enumerate(sorted_children):
                is_last_child = (i == len(sorted_children) - 1)
                new_prefix = "└── " if is_last_child else "├── "
                _print_node(child, level + 1, new_prefix)

        for i, code in enumerate(top_level_codes):
            is_last_top_level = (i == len(top_level_codes) - 1)
            prefix = "└── " if is_last_top_level else "├── "
            _print_node(code, 0, prefix)

    def find_code(self, name: str) -> Code | None:
        """
        Finds a Code object by its name. Case-sensitive.
        Returns the Code object if found, otherwise None.
        """
        # Ensure codes are loaded
        self.codes
        for code_obj in self._codes.values():
            if code_obj.name == name:
                return code_obj
        return None

    @property
    def sources(self) -> dict[str, Source]:
        """
        Retrieves and initializes the sources from the XML if not already done,
        then returns a dictionary of all Source objects by their GUID.
        """
        if not self._sources_initialized_from_xml:
            self._sources = {} # Clear any potential previous state
            sources_tag = self._bs4_obj.find('Sources')
            if sources_tag:
                for source_xml_tag in sources_tag.find_all('TextSource',
                                                           recursive=False):
                    self._parse_source_element(source_xml_tag)
            self._sources_initialized_from_xml = True
        return self._sources

    @sources.setter
    def sources(self, value):
        """
        Dummy setter to warn that direct modification
        of the sources dict is not supported.
        """
        print("Warning: Direct assignment to the 'sources' property "
              "is not supported. Modify sources via Source methods.")

    def _parse_source_element(self, xml_tag: Tag):
        """
        Helper method to parse <TextSource> XML elements
        and create Source objects.
        """
        guid = xml_tag.get('guid')
        name = xml_tag.get('name')
        plain_text_path = xml_tag.get('plainTextPath')
        rich_text_path = xml_tag.get('richTextPath')
        creating_user_guid = xml_tag.get('creatingUser')
        creation_date_time = xml_tag.get('creationDateTime')
        modifying_user_guid = xml_tag.get('modifyingUser')
        modified_date_time = xml_tag.get('modifiedDateTime')

        if not guid or not name or not plain_text_path:
            print("Warning: Skipping malformed TextSource XML "
                  f"tag (missing guid, name, or plainTextPath): {xml_tag}")
            return
        
        try:
            source_obj = Source(
                name=name,
                qde_instance=self,
                guid=guid,
                rich_text_path=rich_text_path,
                creating_user_guid=creating_user_guid,
                creation_date_time=creation_date_time,
                modifying_user_guid=modifying_user_guid,
                modified_date_time=modified_date_time,
                _xml_tag=xml_tag
            )
            self._sources[guid] = source_obj
            # Now, attempt to load the actual text content
            source_obj.text_content = simulate_nvivo_offsets(
                self._qdpx.get_source(guid))

            # remove BOM characters if present
            if (source_obj.text_content
                and source_obj.text_content.startswith('\ufeff')):
                source_obj.text_content = source_obj.text_content[1:]

            if source_obj.text_content is None:
                print("Warning: Could not load plain text "
                      f"content for source '{name}' ({guid}).")

        except ValueError as e:
            print(f"Error creating Source object from XML for '{name}' ({guid}): {e}")

    def _save(self) -> str | None:
        """
        Generates the updated XML content as a string if the project has been
        modified. This method does not directly write to the file system;
        instead, it provides the XML content to be handled by the QDPX class.

        Returns:
            str | None: The complete, formatted XML content as a string if the
                        project was modified. Returns None if no modifications
                        have been made.
        """
        if self.modified:
            # Use .prettify() for a nicely formatted XML string, then encode it
            # to UTF-8 bytes and decode back to string to ensure correct handling
            # of potential encoding nuances, though prettify usually returns str.
            return self._bs4_obj
        return None
    
    def save(self):
        """
        Saves the current state of the QDE project back to the QDPX archive.
        This method should be called after modifications have been made to the
        project, such as adding users or changing metadata.

        It checks if the project has been modified and then uses the QDPX
        object's save_project method to persist changes.
        """
        if self.modified:
            self._qdpx.save_project()
        else:
            print("No modifications to save; project is not marked as modified.")


class QDPX:
    """
    Manages access to the contents of a QDPX (zip-compressed) file.
    It allows listing source files, retrieving their content, and accessing
    the main project.qde XML file, with support for saving modifications
    back to the archive.
    """
    def __init__(self, path: str):
        """
        Initializes the QDPX object with the path to the compressed file.

        Args:
            path (str): The file system path to the .qdpx zip archive.
        """
        self.path = path
        # Stores the QDE object once it's loaded, allowing its 'modified' state
        # to persist across operations.
        self._qde_project: QDE | None = None

    def list_files(self) -> list[str]:
        """
        Lists all files within the QDPX archive, including their paths relative
        to the root of the zip file.

        Returns:
            list[str]: A list of file paths (e.g., 'Sources/guid.txt') within the zip.
                        Returns an empty list if the zip is empty or not valid.
        """
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                return zf.infolist()
        except zipfile.BadZipFile:
            print(f"Error: '{self.path}' is not a valid zip file.")
            return []
        except FileNotFoundError:
            print(f"Error: Zip file not found at '{self.path}'")
            return []
        except Exception as e:
            print(f"An unexpected error occurred while listing files: {e}")
            return []

    def list_sources(self) -> list[str]:
        """
        Lists all plain text source files (ending with .txt) located
        within the 'Sources/' or 'sources/' directory inside the QDPX archive.

        Returns:
            list[str]:
                A list of full paths to plain text source files within the zip
                (e.g., 'Sources/guid.txt'). Returns an empty list if the
                directory is empty, the file doesn't exist, or it's
                not a valid zip file.
        
        Raises:
            FileNotFoundError:
                If the zip file does not contain any source files.
            zipfile.BadZipFile:
                If the provided path is not a valid zip file.
            UnicodeDecodeError:
                If a source file cannot be decoded as UTF-8.
        """
        source_files = []
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                if any(name.startswith('Sources/') for name in zf.namelist()):
                    dirname = 'Sources/'
                elif any(name.startswith('sources/') for name in zf.namelist()):
                    dirname = 'sources/'
                else:
                    raise FileNotFoundError("No sources found in the zip.")

                for name in zf.namelist():
                    # Check if the entry is within 'Sources/' and is a file (not a directory)
                    if (name.startswith(dirname) and name.endswith('.txt') and not name.endswith('/')):
                        # Extract just the basename (e.g., 'guid.txt')
                        source_files.append(name)
        except zipfile.BadZipFile:
            raise zipfile.BadZipFile(
                f"Error: '{self.path}' is not a valid zip file.")
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Error: Zip file not found at '{self.path}'")
        except Exception as e:
            print(f"An unexpected error occurred while listing sources: {e}")
        return source_files

    def get_source(self, guid: str) -> str | None:
        """
        Retrieves the content of a specific source file identified by its GUID.
        The file is expected to be named 'Sources/{guid}.txt' and be UTF-8 encoded.

        Args:
            guid (str): The GUID of the source file to retrieve (e.g.,
                        '4c35014e-8fa9-4e47-b5d1-bfc14a8ddf4f').

        Returns:
            str | None: The decoded UTF-8 content of the source file as a string.
                        Returns None if the file is not found, cannot be decoded,
                        or if any other error occurs during access.
        """
        file_path_in_zip = None  # Initialize to None
        for file_name in self.list_sources():
            if guid in file_name:
                file_path_in_zip = file_name  # Use the full path from the zip
                break
        if not file_path_in_zip:
            print(f"Error: Source file for GUID '{guid}' not found in zip.")
            return None
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                # Open the specified file from the zip archive
                with zf.open(file_path_in_zip, 'r') as source_file:
                    # Read the content and decode it as UTF-8
                    content = source_file.read().decode('utf-8')
                    return content
        except zipfile.BadZipFile:
            print(f"Error: '{self.path}' is not a valid zip file.")
            return None
        except FileNotFoundError:
            print(f"Error: Zip file not found at '{self.path}'")
            return None
        except UnicodeDecodeError:
            print(f"Error: Could not decode '{file_path_in_zip}' as UTF-8. Check encoding.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while getting source '{guid}': {e}")
            return None

    def get_project(self) -> QDE | None:
        """
        Retrieves the QDE project object. If the project XML has already been
        loaded into a QDE object during a previous call, the existing instance
        is returned to preserve its 'modified' state. Otherwise, it reads
        'project.qde' from the zip, parses it, and creates a new QDE object.

        Returns:
            QDE | None: The QDE object representing the project.qde file, or
                        None if the file is not found, cannot be parsed, or
                        any other error occurs.
        """
        # If the QDE project object has already been loaded, return it directly
        if self._qde_project:
            return self._qde_project

        project_file_name = 'project.qde'
        try:
            with zipfile.ZipFile(self.path, 'r') as zf:
                # Open the 'project.qde' file from the zip archive
                with zf.open(project_file_name, 'r') as project_qde_file:
                    # Read and decode the XML content as UTF-8
                    xml_content = project_qde_file.read().decode('utf-8')
                    # Create and store a new QDE object
                    self._qde_project = QDE(xml_content, self)
                    return self._qde_project
        except KeyError:
            print(f"Error: '{project_file_name}' not found in zip. This file is essential.")
            return None
        except zipfile.BadZipFile:
            print(f"Error: '{self.path}' is not a valid zip file.")
            return None
        except FileNotFoundError:
            print(f"Error: Zip file not found at '{self.path}'")
            return None
        except UnicodeDecodeError:
            print(f"Error: Could not decode '{project_file_name}' as UTF-8. Check encoding.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading project.qde: {e}")
            return None

    def save_project(self):
        """
        Saves the current state of the QDE project back into the QDPX zip file.
        This method should be called after modifications have been made to the
        QDE object obtained via `get_project()`. It only performs a save
        operation if the QDE object's `modified` flag is True.

        The process involves:
        1. Getting the updated XML content from the QDE object.
        2. Creating a temporary zip file.
        3. Copying all original files (except 'project.qde') to the temp zip.
        4. Adding the new 'project.qde' content to the temp zip.
        5. Replacing the original zip file with the temporary one.
        6. Resetting the QDE object's `modified` flag.
        """
        if not self._qde_project:
            print("No QDE project object has been loaded. Nothing to save.")
            return

        # Get the new XML content from the QDE object.
        # This will be None if the project hasn't been modified.
        new_xml_content = self._qde_project._save()

        if new_xml_content:
            project_file_name = 'project.qde'
            temp_zip_path = self.path + '.temp_save' # Use a distinct temp name

            try:
                # Ensure the original file exists before attempting to read it
                if not os.path.exists(self.path):
                    raise FileNotFoundError(f"Original zip file not found: {self.path}")

                # Create a temporary zip file and copy contents
                with zipfile.ZipFile(self.path, 'r') as zf_in:
                    with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zf_out:
                        for item in zf_in.namelist():
                            if item != project_file_name:
                                # Copy all existing files except the old project.qde
                                zf_out.writestr(item, zf_in.read(item))
                        # Add the new/modified project.qde content
                        zf_out.writestr(project_file_name, new_xml_content.encode('utf-8'))

                # Atomically replace the original file with the new one
                os.replace(temp_zip_path, self.path)
                print(f"'{project_file_name}' successfully updated in '{self.path}'.")
                # Reset the modified flag of the QDE object after successful save
                self._qde_project.modified = False
            except zipfile.BadZipFile:
                print(f"Error saving: '{self.path}' is not a valid zip file.")
            except FileNotFoundError as e:
                print(f"Error saving: {e}")
            except Exception as e:
                print(f"An unexpected error occurred while saving project.qde to zip: {e}")
                # Clean up the temporary file if an error occurred before successful replacement
                if os.path.exists(temp_zip_path):
                    os.remove(temp_zip_path)
        else:
            print("QDE project was not modified, no save operation performed.")
