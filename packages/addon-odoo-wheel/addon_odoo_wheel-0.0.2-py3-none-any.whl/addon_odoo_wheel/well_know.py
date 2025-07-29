from __future__ import annotations

from abc import ABC, abstractmethod

from manifestoo_core.git_postversion import POST_VERSION_STRATEGY_DOT_N
from manifestoo_core.metadata import OdooSeriesInfo
from manifestoo_core.odoo_series import OdooSeries

_registry_well_know: dict[str | None, WellKnowAddonContributor] = {}


class WellKnowAddonContributor(ABC):
    names = []

    def __init_subclass__(cls, **kwargs):
        assert cls.names
        sub = cls()
        for name in cls.names:
            if name in _registry_well_know:
                raise ValueError(f"Addon contributor {name} already registered")
            _registry_well_know[name and name.upper()] = sub

    @classmethod
    def from_author(cls, name: str | None) -> WellKnowAddonContributor:
        return _registry_well_know.get(name and name.upper() or None) or _UnknownAddonContributor()

    @abstractmethod
    def get_mail(self, odoo_series: OdooSeries | None) -> str: ...

    @abstractmethod
    def get_package_prefix(self, odoo_series: OdooSeries | None) -> str | None: ...

    def git_postversion_strategy(self, odoo_series: OdooSeries | None) -> str:
        if odoo_series:
            return OdooSeriesInfo.from_odoo_series(odoo_series).git_postversion_strategy
        return POST_VERSION_STRATEGY_DOT_N

    def get_classifiers(self, odoo_series: OdooSeries | None) -> list[str]:
        default = [
            "Programming Language :: Python",
            "Framework :: Odoo",
        ]
        if odoo_series:
            default.append(f"Framework :: Odoo :: {odoo_series.value}")
        return default


class _UnknownAddonContributor(WellKnowAddonContributor):
    names = [None, ""]

    def get_mail(self, odoo_serie_info: OdooSeries | None) -> str | None:
        return None

    def get_package_prefix(self, odoo_series: OdooSeries | None) -> str:
        return "addon-odoo"


class _OCAAddonContributor(WellKnowAddonContributor):
    names = ["OCA", "Odoo Community Association (OCA)"]

    def get_mail(self, odoo_serie_info: OdooSeries | None) -> str:
        return "support@odoo-community.org"

    def get_package_prefix(self, odoo_series: OdooSeries | None) -> str:
        return odoo_series and OdooSeriesInfo.from_odoo_series(odoo_series).pkg_name_pfx or "odoo-addon"


class _Mangono(WellKnowAddonContributor):
    names = ["Mangono", "NDP Systemes"]

    def get_mail(self, odoo_serie: OdooSeries | None) -> str:
        return "opensource+odoo@mangono.fr"

    def get_package_prefix(self, odoo_serie: OdooSeries | None) -> str:
        return "mangono-addon"
