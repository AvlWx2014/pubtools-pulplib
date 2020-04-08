import pytest

from pubtools.pulplib import (
    FakeController,
    Criteria,
    RpmUnit,
    ModulemdUnit,
    YumRepository,
)


@pytest.fixture
def controller():
    return FakeController()


@pytest.fixture
def populated_units(controller):
    units1 = [
        RpmUnit(
            name="bash",
            version="4.0",
            release="1",
            arch="x86_64",
            repository_memberships=["repo1"],
        ),
        RpmUnit(
            content_type_id="srpm",
            name="bash",
            version="4.0",
            release="1",
            arch="src",
            repository_memberships=["repo1"],
        ),
        RpmUnit(
            name="glibc",
            version="5.0",
            release="1",
            arch="x86_64",
            repository_memberships=["repo1"],
        ),
        ModulemdUnit(
            name="module1",
            stream="s1",
            version=1234,
            context="a1b2",
            arch="x86_64",
            repository_memberships=["repo1"],
        ),
        ModulemdUnit(
            name="module2",
            stream="s2",
            version=1234,
            context="a1b2",
            arch="x86_64",
            repository_memberships=["repo1"],
        ),
    ]
    units2 = [
        RpmUnit(
            name="glic",
            version="2.3.4",
            release="1",
            arch="x86_64",
            repository_memberships=["repo2"],
        ),
        RpmUnit(
            content_type_id="srpm",
            name="gnu-efi",
            version="3.0c",
            release="1",
            arch="src",
            repository_memberships=["repo2"],
        ),
    ]

    repo1 = YumRepository(id="repo1")
    repo2 = YumRepository(id="repo2")
    controller.insert_repository(repo1)
    controller.insert_units(repo1, units1)
    controller.insert_units(repo2, units2)


def test_search_content_by_type_all(populated_units, controller):
    """search_content_by_type with no criteria specified"""
    units1 = [u for u in controller.client.search_content_by_type("rpm").result()]
    units2 = [u for u in controller.client.search_content_by_type("srpm").result()]
    assert len([u for u in units1 if u.content_type_id == "rpm"]) == 3
    assert len([u for u in units2 if u.content_type_id == "srpm"]) == 2

    assert set(sum([u.repository_memberships for u in units1], [])) == set(
        ["repo1", "repo2"]
    )


def test_search_content_by_type_criteria(populated_units, controller):
    """search_content_by_type with criteria"""
    units1 = [
        u
        for u in controller.client.search_content_by_type(
            "rpm", Criteria.with_field("name", "bash")
        ).result()
    ]
    assert len(units1) == 1


def test_search_content_by_type_criteria_wrong_content_type(populated_units, controller):
    units1 = [
        u
        for u in controller.client.search_content_by_type(
            "srpm", Criteria.with_field("name", "glibc")
        ).result()
    ]
    assert len(units1) == 0
