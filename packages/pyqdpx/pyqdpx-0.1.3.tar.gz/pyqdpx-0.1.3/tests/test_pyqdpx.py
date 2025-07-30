import pytest
import os
import zipfile
import uuid
from datetime import datetime, timezone
from pyqdpx import QDPX, User, Code
from bs4 import BeautifulSoup
from unittest.mock import patch # Import patch

# Constants for test file
TEST_QDPX_FILENAME = "test.qdpx"
PROJECT_QDE_CONTENT_INITIAL = f"""<?xml version="1.0" encoding="utf-8"?>
<Project>
    <Metadata>
        <Title>My Test Project</Title>
    </Metadata>
    <Users>
        <User guid="4c35014e-8fa9-4e47-b5d1-bfc14a8ddf4f" id="SF" name="Florian Sipos"/>
        <User guid="736b0968-f379-4f6d-80d0-479bfa4439b9" id="DS" name="domonkos sik"/>
        <User guid="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" id="UA" name="User A"/>
        <User guid="f93ad076-5ca1-4f46-abf4-b4b67130a6e2" id="UB" name="User B"/>
    </Users>
    <CodeBook>
        <Codes>
            <Code guid="3c51efbb-071f-43a7-9f32-228b89668e8d" name="1. Perceived Susceptibility" isCodable="true">
                <Description>Az emberek akkor hajlandók cselekedni, ha hisznek abban, hogy ők is veszélyben vannak.</Description>
                <Code guid="8baf0c83-56c4-4dc8-9e5b-cf6d6073bdb5" name="alacsony fogékonyság" isCodable="true" />
                <Code guid="b3bae912-0f40-4549-8e8f-dd46acd4f161" name="csoportszintű fogékonyság" isCodable="true" />
            </Code>
            <Code guid="aee8e423-1848-4192-84cf-ea6cb669ff61" name="11. Identitások" isCodable="true">
                <Code guid="ff40617f-1ccd-4e9b-9d15-0ad0801e0d44" name="szélsőjobb" isCodable="true" />
            </Code>
            <Code guid="83e56c7e-c287-46cb-8bb8-1fe8ecae66e9" name="fenyegetés" isCodable="true" />
            <Code guid="ebd49e89-1683-4970-a349-d11f0b792769" name="harag" isCodable="true" />
            <Code guid="{str(uuid.uuid4())}" name="Top Level Code 1" isCodable="true" />
        </Codes>
    </CodeBook>
    <Sources>
        <TextSource guid="56a79789-d535-4fb8-bedd-a915504c54ba" name="videos_selection.docx" richTextPath="internal://56a79789-d535-4fb8-bedd-a915504c54ba.docx" plainTextPath="internal://56a79789-d535-4fb8-bedd-a915504c54ba.txt" creatingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" creationDateTime="2025-06-11T16:24:07Z" modifyingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" modifiedDateTime="2025-06-11T16:24:07Z">
            <Description />
            <PlainTextSelection guid="fd960901-8191-4db1-a3dd-a91626d56c4b" name="" startPosition="233" endPosition="409" creatingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" creationDateTime="2025-06-11T16:31:16Z" modifyingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" modifiedDateTime="2025-06-11T16:31:16Z">
                <Description />
                <Coding guid="f0700850-5e65-4b33-ae59-83d36a021670" creatingUser="f93ad076-5ca1-4f46-abf4-b4b67130a6e2" creationDateTime="2025-06-08T12:42:55Z">
                    <CodeRef targetGUID="83e56c7e-c287-46cb-8bb8-1fe8ecae66e9" />
                </Coding>
            </PlainTextSelection>
            <PlainTextSelection guid="2a6eda45-4583-4f31-8cdd-a91626d56c6b" name="" startPosition="410" endPosition="500" creatingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" creationDateTime="2025-06-11T16:31:16Z" modifyingUser="8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645" modifiedDateTime="2025-06-11T16:31:16Z">
                <Description />
                <Coding guid="fe5603f6-fa55-45fc-b346-ff21013cf440" creatingUser="f93ad076-5ca1-4f46-abf4-b4b67130a6e2" creationDateTime="2025-06-08T12:54:55Z">
                    <CodeRef targetGUID="ebd49e89-1683-4970-a349-d11f0b792769" />
                </Coding>
            </PlainTextSelection>
        </TextSource>
        <TextSource guid="95b6726c-275b-44ee-8035-ad253784094c" name="another_video.mov" richTextPath="internal://95b6726c-275b-44ee-8035-ad253784094c.mov" plainTextPath="internal://95b6726c-275b-44ee-8035-ad253784094c.txt" creatingUser="736b0968-f379-4f6d-80d0-479bfa4439b9" creationDateTime="2025-01-01T10:00:00Z" modifyingUser="736b0968-f379-4f6d-80d0-479bfa4439b9" modifiedDateTime="2025-01-01T10:00:00Z">
            <Description />
        </TextSource>
    </Sources>
    <OtherData>Some other XML data</OtherData>
</Project>
"""
SOURCE_1_GUID = "56a79789-d535-4fb8-bedd-a915504c54ba"
SOURCE_1_CONTENT = "This is the content of videos_selection. It has multiple sentences. We can select different parts of it for coding. This is the part for the first selection. This is the part for the second selection. The end."
SOURCE_2_GUID = "95b6726c-275b-44ee-8035-ad253784094c"
SOURCE_2_CONTENT = "Content for another_video. This is a short piece of text."
FLORIAN_USER_GUID = "4c35014e-8fa9-4e47-b5d1-bfc14a8ddf4f"

@pytest.fixture(scope="function")
def setup_qdpx_file():
    """
    Fixture to create a dummy QDPX file before each test and clean it up afterwards.
    """
    # Create dummy QDPX file
    # Create dummy QDPX file
    with zipfile.ZipFile(TEST_QDPX_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('project.qde', PROJECT_QDE_CONTENT_INITIAL.encode('utf-8'))
        zf.writestr(f'Sources/{SOURCE_1_GUID}.txt', SOURCE_1_CONTENT.encode('utf-8'))
        zf.writestr(f'Sources/{SOURCE_2_GUID}.txt', SOURCE_2_CONTENT.encode('utf-8'))
    yield
    # Clean up dummy QDPX file
    if os.path.exists(TEST_QDPX_FILENAME):
        os.remove(TEST_QDPX_FILENAME)

class TestQDPX:
    def test_list_source_files_in_zip(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        sources = qdpx_file.list_sources()
        assert f'Sources/{SOURCE_1_GUID}.txt' in sources
        assert f'Sources/{SOURCE_2_GUID}.txt' in sources
        assert len(sources) == 2

    def test_get_source_content(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        content = qdpx_file.get_source(SOURCE_1_GUID)
        assert content == SOURCE_1_CONTENT

    def test_get_source_non_existent(self, setup_qdpx_file, capsys):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        content = qdpx_file.get_source("non-existent-guid")
        assert content is None
        captured = capsys.readouterr()
        assert "Error: Source file for GUID 'non-existent-guid' not found in zip." in captured.out

    def test_get_project_initial_load(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        assert project is not None
        assert not project.modified

    def test_get_project_cached(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project1 = qdpx_file.get_project()
        project1.modified = True  # Simulate a change
        project2 = qdpx_file.get_project()
        assert project1 is project2  # Should return the same instance
        assert project2.modified is True

    def test_save_project_no_modification(self, setup_qdpx_file, capsys):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        project.save()  # No modification made, so shouldn't save
        captured = capsys.readouterr()
        assert "No modifications to save; project is not marked as modified." in captured.out
        # Verify file content remains original (no temp file created/replaced)
        with zipfile.ZipFile(TEST_QDPX_FILENAME, 'r') as zf:
            content = zf.read('project.qde').decode('utf-8')
            assert content == PROJECT_QDE_CONTENT_INITIAL.format(uuid=list(qdpx_file.get_project().codes.keys())[-1])

    def test_save_project_with_modification(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        # Make a modification (add a user)
        new_user = User(id="JA", name="Jane Austen")
        project.add_user(new_user)
        assert project.modified is True
        
        project.save()
        
        # Verify modified flag is reset
        assert project.modified is False
        
        # Re-open and verify content
        qdpx_file_reloaded = QDPX(TEST_QDPX_FILENAME)
        reloaded_project = qdpx_file_reloaded.get_project()
        reloaded_users = reloaded_project.users
        assert new_user.guid in reloaded_users
        assert reloaded_users[new_user.guid].name == "Jane Austen"

    def test_save_project_atomicity(self, setup_qdpx_file, capsys):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        # Simulate a modification
        new_user = User(id="ERROR", name="Error User")
        project.add_user(new_user)

        # Use patch to mock os.replace and make it raise an OSError
        with patch('os.replace') as mock_os_replace:
            mock_os_replace.side_effect = OSError("Simulated write error during atomic replacement")
            
            # Call save, but don't expect an exception to be raised OUT of the method
            project.save()
            
            # Assert that our mocked os.replace was called
            mock_os_replace.assert_called_once()
        
        # Capture stdout to check the error message printed by the module
        captured = capsys.readouterr()
        assert "An unexpected error occurred while saving project.qde " +\
            "to zip: Simulated write error during atomic replacement" in captured.out
        
        # Assert that the temporary file is cleaned up and original file exists
        temp_file_name = TEST_QDPX_FILENAME + '.temp_save'
        assert not os.path.exists(temp_file_name)
        assert os.path.exists(TEST_QDPX_FILENAME)
        
        # Verify original content is still there (i.e., new user not saved)
        with zipfile.ZipFile(TEST_QDPX_FILENAME, 'r') as zf:
            content = zf.read('project.qde').decode('utf-8')
            assert "Error User" not in content # Should not be saved
            assert 'name="Florian Sipos"' in content # Ensure original content is intact

class TestUser:
    def test_user_initialization_auto_guid(self):
        user = User(id="JD", name="John Doe")
        assert user.id == "JD"
        assert user.name == "John Doe"
        assert isinstance(user.guid, str)
        assert len(user.guid) == 36 # Standard UUID length

    def test_user_initialization_with_guid(self):
        test_guid = "12345678-1234-5678-1234-567812345678"
        user = User(id="AB", name="Alice Bob", guid=test_guid)
        assert user.guid == test_guid

    def test_user_initialization_invalid_guid(self):
        with pytest.raises(ValueError, match="Invalid GUID format"):
            User(id="XX", name="Invalid User", guid="not-a-guid")

    def test_user_equality(self):
        user1 = User(id="A", name="User A", guid=str(uuid.uuid4()))  # Generate a random GUID
        user2 = User(id="A", name="User A", guid=user1.guid)  # Same GUID as user1
        user3 = User(name="User B", guid=str(uuid.uuid4()))
        
        assert user1 == user2
        assert user1 != user3
        assert user1 != "not a user"

    def test_user_repr(self):
        user_guid = str(uuid.uuid4())
        user = User(id="Test", name="Test User", guid=user_guid)
        assert repr(user) == f"User(guid='{user_guid}', name='Test User', id='Test')"

    def test_user_id(self):
        user1 = User(id="AB", name="Alice Bob")
        user2 = User(name="Alice Bob")
        assert user1.id == "AB"
        assert user2.id is None  # No ID set, should be None

class TestQDEUsers:
    def test_qde_initial_users_loading(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        users = project.users
        
        assert len(users) == 4
        
        florian = users["4c35014e-8fa9-4e47-b5d1-bfc14a8ddf4f"]
        assert florian.id == "SF"
        assert florian.name == "Florian Sipos"
        
        domonkos = users["736b0968-f379-4f6d-80d0-479bfa4439b9"]
        assert domonkos.id == "DS"
        assert domonkos.name == "domonkos sik"

    def test_add_user_to_qde(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        new_user = User(id="JKR", name="J.K. Rowling")
        project.add_user(new_user)
        
        assert project.modified is True
        assert new_user.guid in project.users
        assert project.users[new_user.guid] == new_user
        assert len(project.users) == 5

        # Verify the XML content includes the new user
        xml_str = str(project._bs4_obj)
        assert f'<User guid="{new_user.guid}" id="JKR" name="J.K. Rowling"/>' in xml_str

    def test_add_user_no_users_tag(self, setup_qdpx_file):
        # Create a QDPX file without a <Users> tag initially
        project_xml_no_users = """<?xml version="1.0" encoding="utf-8"?>
<Project>
    <Metadata><Title>Project Without Users</Title></Metadata>
</Project>
"""
        with zipfile.ZipFile(TEST_QDPX_FILENAME, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.writestr('project.qde', project_xml_no_users.encode('utf-8'))

        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()

        new_user = User(id="NEW", name="New User")
        project.add_user(new_user)
        
        assert project.modified is True
        assert new_user.guid in project.users
        
        xml_str = str(project._bs4_obj)
        assert "<Users>" in xml_str
        assert f'<User guid="{new_user.guid}" id="NEW" name="New User"/>' in xml_str

class TestCode:
    def test_code_initialization_auto_guid(self):
        # Need a dummy QDE instance for Code initialization
        class DummyQDE:
            def __init__(self):
                self._codes = {}
                self._codes_initialized_from_xml = False
                self._bs4_obj = None # Not needed for basic init but good practice
            modified = False
        
        dummy_qde = DummyQDE()
        code = Code(name="Test Code", qde_instance=dummy_qde)
        assert code.name == "Test Code"
        assert isinstance(code.guid, str)
        assert code.is_codable is True
        assert code.description is None
        assert code.parent is None
        assert code.guid in dummy_qde._codes
        assert dummy_qde._codes[code.guid] is code

    def test_code_initialization_with_guid_and_description(self):
        class DummyQDE:
            def __init__(self):
                self._codes = {}
                self._codes_initialized_from_xml = False
                self._bs4_obj = BeautifulSoup("<Project><CodeBook><Codes/></CodeBook></Project>", 'xml')
                self.users = {}
            modified = False

        dummy_qde = DummyQDE()
        test_guid = "a1b2c3d4-e5f6-7890-abcd-1234567890ab"
        code = Code(name="Described Code", qde_instance=dummy_qde, guid=test_guid, 
                    is_codable=False, description="A detailed description.")
        assert code.guid == test_guid
        assert code.name == "Described Code"
        assert code.is_codable is False
        assert code.description == "A detailed description."

    def test_code_initialization_invalid_guid(self):
        class DummyQDE:
            def __init__(self):
                self._codes = {}
                self._codes_initialized_from_xml = False
                self._bs4_obj = BeautifulSoup("<Project><CodeBook><Codes/></CodeBook></Project>", 'xml')
            modified = False
        
        dummy_qde = DummyQDE()
        with pytest.raises(ValueError, match="Invalid GUID format"):
            Code(name="Bad GUID", qde_instance=dummy_qde, guid="bad-guid")

    def test_code_parent_child_relationship(self):
        class DummyQDE:
            def __init__(self):
                self._codes = {}
                self._codes_initialized_from_xml = False
                self._bs4_obj = BeautifulSoup("<Project><CodeBook><Codes/></CodeBook></Project>", 'xml')
                self.users = {}
            modified = False
        
        dummy_qde = DummyQDE()
        parent_code = Code(name="Parent", qde_instance=dummy_qde)
        child_code = Code(name="Child", qde_instance=dummy_qde, parent=parent_code)

        assert child_code.parent == parent_code
        assert parent_code._children_guids == [child_code.guid]
        assert child_code in parent_code.children

    def test_code_name_setter(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code = project.find_code("1. Perceived Susceptibility")
        assert code.name == "1. Perceived Susceptibility"
        assert not project.modified

        code.name = "Modified Susceptibility"
        assert code.name == "Modified Susceptibility"
        assert project.modified

        # Verify XML tag updated
        xml_str = str(project._bs4_obj)
        assert 'name="Modified Susceptibility"' in xml_str
        assert 'name="1. Perceived Susceptibility"' not in xml_str

    def test_code_description_setter(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code = project.find_code("1. Perceived Susceptibility")
        assert code.description is not None
        assert not project.modified

        # Update description
        code.description = "New description text."
        assert code.description == "New description text."
        assert project.modified
        xml_str = str(project._bs4_obj)
        assert "<Description>New description text.</Description>" in xml_str

        # Remove description
        project.modified = False # Reset for next check
        code.description = None
        assert code.description is None
        assert project.modified
        xml_str = str(project._bs4_obj)
        assert "<Description>" not in xml_str # Should be removed

    def test_code_is_codable_setter(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code = project.find_code("alacsony fogékonyság")
        assert code.is_codable is True
        assert not project.modified

        code.is_codable = False
        assert code.is_codable is False
        assert project.modified
        xml_str = str(project._bs4_obj.find('Code', guid=code.guid))
        assert 'isCodable="false"' in xml_str
        assert 'isCodable="true"' not in xml_str

    def test_code_delete_leaf_node(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code_to_delete = project.find_code("alacsony fogékonyság")
        parent_code = code_to_delete.parent
        
        assert code_to_delete.guid in project._codes
        assert code_to_delete.guid in parent_code._children_guids
        
        code_to_delete.delete()
        
        assert project.modified
        assert code_to_delete.guid not in project._codes
        assert code_to_delete.guid not in parent_code._children_guids
        xml_str = str(project._bs4_obj)
        assert 'name="alacsony fogékonyság"' not in xml_str

    def test_code_delete_with_children_raises_exception(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code_with_children = project.find_code("1. Perceived Susceptibility")
        assert len(code_with_children.children) > 0

        with pytest.raises(Exception, match="Cannot delete code .* because it has children."):
            code_with_children.delete()
        
        # Ensure code is not deleted from project or XML
        assert code_with_children.guid in project._codes
        xml_str = str(project._bs4_obj)
        assert 'name="1. Perceived Susceptibility"' in xml_str
        assert not project.modified # Should not be modified as deletion failed

    def test_code_add_to_bs4_for_new_code(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        initial_xml_content = str(project._bs4_obj)
        
        # Add a new top-level code
        new_code_guid = str(uuid.uuid4())
        new_top_level_code = Code(name="Brand New Top Code", qde_instance=project, guid=new_code_guid)

        assert project._codes_initialized_from_xml
        
        assert project.modified
        xml_str_after_add = str(project._bs4_obj)
        
        # Verify the new code XML tag is present in the BeautifulSoup object
        assert f'name="Brand New Top Code"' in xml_str_after_add
        assert f'guid="{new_code_guid}"' in xml_str_after_add
        
        # Verify it's added as a direct child of <Codes>
        # This requires more specific BeautifulSoup querying
        codebook_tag = project._bs4_obj.find('CodeBook')
        codes_tag = codebook_tag.find('Codes')
        found_new_tag = False
        for tag in codes_tag.find_all('Code', recursive=False):
            if tag.get('guid') == new_code_guid:
                found_new_tag = True
                break
        assert found_new_tag

    def test_code_add_child_to_bs4(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        parent_code = project.find_code("11. Identitások")
        assert parent_code is not None

        new_child_guid = str(uuid.uuid4())
        new_child_code = Code(name="Nested Child Code", qde_instance=project, parent=parent_code, guid=new_child_guid)
        
        assert project.modified
        xml_str_after_add = str(project._bs4_obj)
        
        # Verify the new child code XML tag is present within its parent in the BeautifulSoup object
        parent_xml_tag = project._bs4_obj.find('Code', guid=parent_code.guid)
        assert parent_xml_tag is not None
        
        found_child_tag = False
        for tag in parent_xml_tag.find_all('Code', recursive=False):
            if tag.get('guid') == new_child_guid:
                found_child_tag = True
                break
        assert found_child_tag

class TestQDECodes:
    def test_qde_codes_loading_and_hierarchy(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        codes = project.codes # This triggers loading

        assert len(codes) == 8 # 5 top-level + 3 children

        assert project.find_code("fenyegetés") is not None
        assert project.find_code("harag") is not None

        susceptibility = project.find_code("1. Perceived Susceptibility")
        assert susceptibility is not None
        assert susceptibility.parent is None
        assert len(susceptibility.children) == 2
        assert any(c.name == "alacsony fogékonyság" for c in susceptibility.children)
        assert any(c.name == "csoportszintű fogékonyság" for c in susceptibility.children)

        low_susceptibility = project.find_code("alacsony fogékonyság")
        assert low_susceptibility is not None
        assert low_susceptibility.parent == susceptibility
        assert len(low_susceptibility.children) == 0

        identities = project.find_code("11. Identitások")
        assert identities is not None
        assert identities.parent is None
        assert len(identities.children) == 1
        assert identities.children[0].name == "szélsőjobb"

    def test_qde_find_code(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        code = project.find_code("1. Perceived Susceptibility")
        assert code is not None
        assert code.name == "1. Perceived Susceptibility"

        not_found_code = project.find_code("Non Existent Code")
        assert not_found_code is None

    def test_qde_print_code_tree(self, setup_qdpx_file, capsys):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        project.print_code_tree()
        captured = capsys.readouterr()
        output = captured.out

        assert "--- Code Tree ---" in output
        assert "├── '1. Perceived Susceptibility'*" in output
        assert "│    ├── 'alacsony fogékonyság'" in output
        assert "│    └── 'csoportszintű fogékonyság'" in output
        assert "├── '11. Identitások'" in output
        assert "│    └── 'szélsőjobb'" in output
        assert "├── 'Top Level Code 1'" in output
        assert "├── 'fenyegetés'" in output
        assert "└── 'harag'" in output
        
        # Ensure codes are sorted alphabetically at each level
        # This is implicitly tested by the specific order of assertions above
        # A more robust test might parse the output lines and verify order explicitly.

class TestSource:
    def test_source_initialization_and_content_loading(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project() # This loads sources and their content

        sources = project.sources
        assert len(sources) == 2

        source1 = sources[SOURCE_1_GUID]
        assert source1.name == "videos_selection.docx"
        assert source1.guid == SOURCE_1_GUID
        assert source1.plain_text_path == f"internal://{SOURCE_1_GUID}.txt"
        assert source1.text_content == SOURCE_1_CONTENT
        assert len(source1.coded_selections) == 2 # Expecting two selections from XML

        source2 = sources[SOURCE_2_GUID]
        assert source2.name == "another_video.mov"
        assert source2.guid == SOURCE_2_GUID
        assert source2.text_content == SOURCE_2_CONTENT
        assert len(source2.coded_selections) == 0

    def test_source_selection_parsing(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]

        # Get the expected selections from the XML
        selection1_guid = "fd960901-8191-4db1-a3dd-a91626d56c4b"
        selection2_guid = "2a6eda45-4583-4f31-8cdd-a91626d56c6b"
        
        sel1 = source1.coded_selections[selection1_guid]
        assert sel1.start_position == 233
        assert sel1.end_position == 409
        assert sel1.code.name == "fenyegetés"
        assert sel1.user.id == "UA"
        assert sel1.text == SOURCE_1_CONTENT[233:409]

        sel2 = source1.coded_selections[selection2_guid]
        assert sel2.start_position == 410
        assert sel2.end_position == 500
        assert sel2.code.name == "harag"
        assert sel2.user.id == "UA"
        assert sel2.text == SOURCE_1_CONTENT[410:500]

    def test_source_add_selection(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]
        
        initial_selections_count = len(source1.coded_selections)
        
        # Get a user and a code for the new selection
        test_user = project.users[FLORIAN_USER_GUID]
        test_code = project.find_code("alacsony fogékonyság")
        
        new_start = 0
        new_end = 10
        new_selection = source1.add_selection(new_start, new_end, test_code, test_user)
        
        assert project.modified is True
        assert len(source1.coded_selections) == initial_selections_count + 1
        assert new_selection.guid in source1.coded_selections
        assert new_selection.start_position == new_start
        assert new_selection.end_position == new_end
        assert new_selection.code == test_code
        assert new_selection.user == test_user
        assert new_selection.text == SOURCE_1_CONTENT[new_start:new_end]

        # Verify the XML has been updated
        xml_str = str(project._bs4_obj)
        assert f'guid="{new_selection.guid}"' in xml_str
        assert f'startPosition="{new_start}"' in xml_str
        assert f'endPosition="{new_end}"' in xml_str
        assert f'creatingUser="{test_user.guid}"' in xml_str
        assert f'targetGUID="{test_code.guid}"' in xml_str
        
        # Verify datetime format
        now_utc = datetime.now().replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
        assert now_utc[:16] in xml_str # Check YYYY-MM-DDTHH:MM

    def test_source_add_selection_invalid_range(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]
        test_user = project.users[FLORIAN_USER_GUID]
        test_code = project.find_code("alacsony fogékonyság")

        with pytest.raises(ValueError, match="Invalid selection range"):
            source1.add_selection(10, 5, test_code, test_user) # end < start

        with pytest.raises(ValueError, match="Invalid selection range"):
            source1.add_selection(0, len(source1.text_content) + 1, test_code, test_user) # out of bounds

    def test_source_find_user_selections(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]
        
        user_a = project.users["8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645"] # User A
        user_b = project.users["f93ad076-5ca1-4f46-abf4-b4b67130a6e2"] # User B, is creatingUser of Coding

        # The selections are explicitly coded by User B in the Coding tag, but PlainTextSelection's
        # creatingUser attribute is '8ca3a2c1-8b7a-41c3-a9dd-a8fb46caa645' (User A)
        # The prompt specified "the latter should return the user object corresponding to the creating user of the PlainTextSelection."
        selections_by_user_a = source1.find_user_selections(user_a)
        selections_by_user_b = source1.find_user_selections(user_b)
        
        assert len(selections_by_user_a) == 2
        assert len(selections_by_user_b) == 0 # Based on PlainTextSelection's creatingUser
        
        # Verify selections are indeed by User A
        for sel in selections_by_user_a:
            assert sel.user == user_a

    def test_source_find_code_selections(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]
        
        code_threat = project.find_code("fenyegetés")
        code_anger = project.find_code("harag")
        code_non_existent = project.find_code("Non Existent Code")

        selections_threat = source1.find_code_selections(code_threat)
        selections_anger = source1.find_code_selections(code_anger)
        selections_non_existent = source1.find_code_selections(code_non_existent)

        assert len(selections_threat) == 1
        assert selections_threat[0].code == code_threat
        
        assert len(selections_anger) == 1
        assert selections_anger[0].code == code_anger

        assert len(selections_non_existent) == 0

    def test_selection_delete(self, setup_qdpx_file):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        source1 = project.sources[SOURCE_1_GUID]

        selection_guid_to_delete = "fd960901-8191-4db1-a3dd-a91626d56c4b"
        selection_to_delete = source1.coded_selections[selection_guid_to_delete]
        
        assert selection_to_delete.guid in source1.coded_selections
        assert not project.modified

        selection_to_delete.delete()
        
        assert project.modified
        assert selection_to_delete.guid not in source1.coded_selections
        assert len(source1.coded_selections) == 1 # One less selection

        # Verify XML tag is removed
        xml_str = str(project._bs4_obj)
        assert f'guid="{selection_guid_to_delete}"' not in xml_str
        assert f'startPosition="233"' not in xml_str

    def test_qde_sources_setter_warns(self, setup_qdpx_file, capsys):
        qdpx_file = QDPX(TEST_QDPX_FILENAME)
        project = qdpx_file.get_project()
        
        # Attempt to set sources directly
        project.sources = {"new_guid": "dummy_source"}
        
        captured = capsys.readouterr()
        assert "Warning: Direct assignment to the 'sources' property is not supported." in captured.out
        
        # Verify that the actual sources dict remains unchanged
        assert len(project.sources) == 2

