# pylint: disable=unused-import

# Third Party Libraries
import pytest

from dictns import Namespace

# Gitlab-Project-Configurator Modules
from gpc.general_executor import GpcGeneralExecutor
from gpc.helpers.types import GroupPathRule
from gpc.helpers.types import ProjectPathRule
from gpc.project_rule_executor import GroupRuleExecutor


# pylint: disable=redefined-outer-name


@pytest.fixture
def fake_gpc_params(mocker):
    fake_params = mocker.Mock()
    fake_params.groups = None
    fake_params.projects = None
    fake_params.report_file = None
    yield fake_params


def test_not_seen_yet_only(mocker, fake_gitlab, fake_gpc_params):
    gpc = GpcGeneralExecutor(parameters=fake_gpc_params, gitlab=fake_gitlab)
    mocker.patch(
        "gpc.tests.test_group_listing.GpcGeneralExecutor.raw_config",
        mocker.PropertyMock(return_value={}),
    )
    mocker.patch("gpc.tests.test_group_listing.GroupRuleExecutor.execute", mocker.Mock())
    group_path = "a/group/path"
    fake_rule = Namespace({"name": "fakerule"})

    def gen_grp_rule():
        yield GroupPathRule(
            group_path=group_path + "/group_1",
            rule=fake_rule,
            recursive=False,
            not_seen_yet_only=False,
        )
        for i in range(5):
            fake_grp_name = group_path + f"/group_{i}"
            yield GroupPathRule(
                group_path=fake_grp_name,
                rule=fake_rule,
                recursive=False,
                not_seen_yet_only=True,
            )

    lst = list(gpc._handle_group_exclusion(gen_grp_rule()))  # pylint: disable=protected-access
    lst_groups = [g.group_path for g in lst]
    assert lst_groups == [
        "a/group/path/group_1",
        "a/group/path/group_0",
        "a/group/path/group_2",
        "a/group/path/group_3",
        "a/group/path/group_4",
    ]
    assert lst_groups.count("a/group/path/group_1") == 1


def test_group_exclusion(mocker, fake_gitlab, fake_gpc_params):
    gpc = GpcGeneralExecutor(parameters=fake_gpc_params, gitlab=fake_gitlab)
    group_path = "a/group/path"

    fake_rule = Namespace({"name": "fakerule"})
    group_excludes = [
        "a/group/path/group_1",
        "a/group/path/lvl1_1/sub_g",
        "a/group/path/lvl1_2/lvl2/sub_group_to_exclude",
        "^.*exclude_through_regex$",
    ]

    def gen_grp_rule():
        # Groups:
        # a/group/path/group_0                                        | kept
        # a/group/path/group_1                                        | exclude
        # a/group/path/group_2                                        | kept
        # a/group/path/group_3                                        | kept
        # a/group/path/group_4                                        | kept
        # a/group/path/                                               | kept
        # a/group/path/lvl1_1                                         | kept
        # a/group/path/lvl1_1/sub_g/p1                                | exclude
        # a/group/path/lvl1_1/sub_p_v1                                | kept
        # a/group/path/lvl1_2/lvl2/sub_group_to_exclude/group1      | exclude
        # a/group/path/lvl1_2/lvl2/sub_group_to_keep/group1_kept    | kept
        # a/group/path/a/group/to/exclude_through_regex               | exclude
        for i in range(5):
            fake_grp_name = group_path + f"/group_{i}"
            yield GroupPathRule(
                group_path=fake_grp_name,
                rule=fake_rule,
                recursive=False,
                excludes=group_excludes,
                not_seen_yet_only=True,
            )

        yield GroupPathRule(
            group_path=group_path + "/",
            rule=fake_rule,
            recursive=True,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

        yield GroupPathRule(
            group_path="a/group/path/lvl1_1/sub_g/g1",
            rule=fake_rule,
            recursive=False,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

        yield GroupPathRule(
            group_path="a/group/path/lvl1_1/sub_g_v1",
            rule=fake_rule,
            recursive=False,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

        yield GroupPathRule(
            group_path="a/group/path/lvl1_2/lvl2/sub_group_to_exclude/group1",
            rule=fake_rule,
            recursive=False,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

        yield GroupPathRule(
            group_path="a/group/path/lvl1_2/lvl2/sub_group_to_keep/group1_kept",
            rule=fake_rule,
            recursive=False,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

        yield GroupPathRule(
            group_path="a/group/path/a/group/to/exclude_through_regex",
            rule=fake_rule,
            recursive=False,
            excludes=group_excludes,
            not_seen_yet_only=True,
        )

    matcher = mocker.Mock(name="fake_matcher")
    matcher.find_rules = mocker.Mock("find_rules", side_effect=gen_grp_rule)

    def mk_fake_group(full_path):
        g = mocker.Mock(name=full_path)
        g.full_path = full_path
        return g

    def fake_get_group(_gl, wanted_group):
        fake_base_group_path = mocker.Mock(name="a/group/path")
        fake_base_group_path.subgroups = mocker.Mock(name="fake_a_group_path.subgroups")
        fake_base_group_path.subgroups.list = mocker.Mock(
            name="fake_a_group_path.list.subgroups",
            return_value=[
                mk_fake_group("a/group/path/group_0"),
                mk_fake_group("a/group/path/group_1"),
                mk_fake_group("a/group/path/group_2"),
                mk_fake_group("a/group/path/group_3"),
                mk_fake_group("a/group/path/group_4"),
            ],
        )
        fake_base_group_path.subgroups = mocker.Mock(name="fake_a_group_path.subgroups")
        a_group_path_lvl1_1_sub_g = mocker.Mock(name="a_group_path_lvl1_1_sub_g")
        a_group_path_lvl1_1_sub_g.full_path = "a/group/path/lvl1_1/sub_g"
        a_group_path_lvl1_1_sub_g.subgroups.list = mocker.Mock(
            name="a_group_path_lvl1_1_sub_g.groups.list",
            return_value=[mk_fake_group("a/group/path/lvl1_1/sub_g/g1")],
        )
        a_group_path_lvl1_1_sub_g.subgroups.list = mocker.Mock(
            name="a_group_path_lvl1_1_sub_g.subgroups.list", return_value=[]
        )

        a_group_path_lvl1_1 = mocker.Mock(name="a_group_path_lvl1_1")
        a_group_path_lvl1_1.full_path = "a/group/path/lvl1_1"
        a_group_path_lvl1_1.groups.list = mocker.Mock(
            name="a_group_path_lvl1_1.subgroups.list",
            return_value=[
                mk_fake_group("a/group/path/lvl1_1/sub_g_v1"),
            ],
        )
        a_group_path_lvl1_1.subgroups.list = mocker.Mock(
            name="a_group_path_lvl1_1.subgroups.list",
            return_value=[
                a_group_path_lvl1_1_sub_g,
            ],
        )
        base_group_path_subgroups = [a_group_path_lvl1_1]
        fake_base_group_path.subgroups.list = mocker.Mock(
            name="fake_base_group_path.subgroups.list", return_value=base_group_path_subgroups
        )

        groups = {
            "a/group/path": fake_base_group_path,
            "a/group/path/lvl1_1": a_group_path_lvl1_1,
            "a/group/path/lvl1_1/sub_g": a_group_path_lvl1_1_sub_g,
        }
        return groups[wanted_group]

    def fake_is_path_a_group(wanted_path):
        is_a_group = {
            "a/group/path/group_0": False,
            "a/group/path/group_1": False,
            "a/group/path/group_2": False,
            "a/group/path/group_3": False,
            "a/group/path/group_4": False,
            "a/group/path": True,
            "a/group/path/lvl1_1": True,
            "a/group/path/lvl1_1/sub_p": True,
            "a/group/path/lvl1_1/sub_p/p1": False,
            "a/group/path/lvl1_1/sub_g_v1": False,
            "a/group/path/lvl1_2/lvl2/sub_group_to_exclude/group1": False,
            "a/group/path/lvl1_2/lvl2/sub_group_to_keep/group1_kept": False,
            "a/group/path/a/group/to/exclude_through_regex": False,
        }
        return is_a_group[wanted_path]

    mocker.patch.object(gpc, "_is_path_a_group", side_effect=fake_is_path_a_group)
    mocker.patch("gpc.general_executor.get_group", side_effect=fake_get_group)
    lst = list(gpc.iter_on_groups_with_rules(matcher))

    lst_groups = [g.group_path for g in lst]

    assert lst_groups == [
        "a/group/path/group_0",
        "a/group/path/group_2",
        "a/group/path/group_3",
        "a/group/path/group_4",
        "a/group/path/lvl1_1",
        "a/group/path/",
        "a/group/path/lvl1_1/sub_g_v1",
        "a/group/path/lvl1_2/lvl2/sub_group_to_keep/group1_kept",
    ]
    assert "a/group/path/group_1" not in lst_groups
    assert "a/group/path/a/group/to/exclude_through_regex" not in lst_groups


def test_with_duplicate(mocker, fake_gitlab, fake_gpc_params):
    def fake_is_path_a_group(p: str) -> bool:
        return p.strip("/") == group_path

    gpc = GpcGeneralExecutor(parameters=fake_gpc_params, gitlab=fake_gitlab)
    group_path = "a/group"
    fake_group_list = [
        Namespace(
            {
                "full_path": group_path + "/matched_group1",
                "shared_with_groups": [],
            }
        ),
        Namespace(
            {
                "full_path": group_path + "/found_group2",
                "shared_with_groups": [],
            }
        ),
    ]
    fake_group = mocker.Mock("fake_group")
    fake_group.full_path = group_path
    fake_group.subgroups = mocker.Mock("fake_subgroups")
    fake_group.subgroups.list = mocker.Mock("subgroup_list", return_value=fake_group_list)
    mocker.patch.object(fake_gitlab.groups, "get", return_value=fake_group)

    mocker.patch.object(gpc, "_is_path_a_group", side_effect=fake_is_path_a_group)
    fake_rule = Namespace({"a_fake": "rule"})

    def gen_grp_rule():
        for i in range(5):
            fake_grp_name = group_path + f"/group_{i}"
            yield GroupPathRule(
                group_path=fake_grp_name,
                rule=fake_rule,
                recursive=False,
                not_seen_yet_only=False,
            )
        yield GroupPathRule(
            group_path=group_path + "/",
            rule=fake_rule,
            recursive=False,
            not_seen_yet_only=False,
        )
        # Just to verify group_path + '/matched_group1' isn't twice in the result
        yield GroupPathRule(
            group_path=group_path + "/matched_group1",
            rule=fake_rule,
            recursive=False,
            not_seen_yet_only=False,
        )

    fake_matcher = mocker.Mock()
    fake_matcher.find_rules = gen_grp_rule
    lst = list(gpc.iter_on_groups_with_rules(fake_matcher))

    assert lst == [
        GroupPathRule(
            group_path="a/group/group_0",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/group_1",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/group_2",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/group_3",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/group_4",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
        GroupPathRule(
            group_path="a/group/matched_group1",
            rule={"a_fake": "rule"},
            recursive=False,
            not_seen_yet_only=False,
        ),
    ]

    # There is only 1 instance of 'a/group/matched_group1'
