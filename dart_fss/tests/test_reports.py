import pytest

from ..search import search_report_with_cache


@pytest.fixture(scope='module')
def last_report():
    crp_cd = '005930'
    return search_report_with_cache(crp_cd=crp_cd, start_dt='20180101', end_dt='20190101', bsn_tp='a001')[0]


def test_reports(last_report):
    actual = last_report.rcp_no
    expected = '20180402005019'
    assert actual == expected


def test_reports_pages(last_report):
    first_page = last_report[0]
    actual = first_page.ele_id
    expected = 0
    assert actual == expected


def test_reports_to_dict(last_report):
    results = last_report.to_dict()
    actual = results['crp_nm']
    expected = '삼성전자'
    assert actual == expected


def test_reports_xbrl(last_report):
    xbrl_file = last_report.xbrl.filename
    assert xbrl_file is not None


def test_reports_find_all(last_report):
    query = {
        'includes': '전문가 AND 확인',
        'excludes': '1'
    }
    page = last_report.find_all(**query)['pages'][0]
    actual = page.dcm_no
    expected = '6060273'
    assert actual == expected


def test_reports_to_dict(last_report):
    info = last_report.to_dict(summary=False)
    actual = info.get('xbrl')
    expected = 'IFRS(원문XBRL)(20180402005019_ifrs.zip)'
    assert actual == expected


def test_reports_replated_reports():
    crp_cd='000660'
    report = search_report_with_cache(crp_cd=crp_cd, start_dt='20180101', end_dt='20190101', bsn_tp='a001')[0]
    report.load()
    related_reports = report.related_reports
    actual = len(related_reports)
    expected = 1
    assert actual == expected


def test_reports_find_all():
    crp_cd='000660'
    report = search_report_with_cache(crp_cd=crp_cd, start_dt='20180101', end_dt='20190101', bsn_tp='a001')[0]
    query = {
        'includes': '전문가 AND 확인',
        'excludes': '1'
    }
    page = report.find_all(**query)['pages'][0]
    actual = page.dcm_no
    expected = '6217166'
    assert actual == expected

