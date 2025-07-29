import random
import socket
import uiautomator2 as u2
import types
import rtree
import re
from typing import Dict, List, Union
from lxml import etree
from .absDriver import AbstractScriptDriver, AbstractStaticChecker, AbstractDriver
from .adbUtils import list_forwards, remove_forward, create_forward
from .utils import TimeStamp, getLogger

TIME_STAMP = TimeStamp().getTimeStamp()

import logging
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("uiautomator2").setLevel(logging.INFO)

logger = getLogger(__name__)

"""
The definition of U2ScriptDriver
"""
class U2ScriptDriver(AbstractScriptDriver):
    """
    This is the ScriptDriver used to send ui automation request in Property
    When you interact with the mobile in properties. You will use the object here
    
    *e.g. the following self.d use U2ScriptDriver*
    ```
    @precondition(...)
    def test_battery(self):
        self.d(text="battery").click()
    ```
    """

    deviceSerial: str = None
    d = None

    @classmethod
    def setDeviceSerial(cls, deviceSerial):
        cls.deviceSerial = deviceSerial

    def getInstance(self):
        if self.d is None:
            self.d = (
                u2.connect() if self.deviceSerial is None
                else u2.connect(self.deviceSerial)
            )

            def get_u2_forward_port() -> int:
                """rewrite forward_port mothod to avoid the relocation of port
                :return: the new forward port
                """
                print("Rewriting forward_port method", flush=True)
                self.d._dev.forward_port = types.MethodType(
                                forward_port, self.d._dev)
                lport = self.d._dev.forward_port(8090)
                setattr(self.d._dev, "msg", "meta")
                print(f"[U2] local port: {lport}", flush=True)
                return lport

            self._remove_remote_port(8090)
            self.d.lport = get_u2_forward_port()
            self._remove_remote_port(9008)

        return self.d

    def _remove_remote_port(self, port:int):
        """remove the forward port
        """
        forwardLists = list_forwards(device=self.deviceSerial)
        for forward in forwardLists:
            if forward["remote"] == f"tcp:{port}":
                forward_local = forward["local"]
                remove_forward(local_spec=forward_local, device=self.deviceSerial)

    def tearDown(self):
        logger.debug("U2Driver tearDown: stop_uiautomator")
        self.d.stop_uiautomator()
        logger.debug("U2Driver tearDown: remove forward")
        self._remove_remote_port(8090)

"""
The definition of U2StaticChecker
"""
class StaticU2UiObject(u2.UiObject):
    def __init__(self, session, selector):
        self.session: U2StaticDevice = session
        self.selector = selector

    def _transferU2Keys(self, originKey):
        filterDict = {
            "resourceId": "resource-id",
            "description": "content-desc",
            "className": "class",
            "longClickable": "long-clickable",
        }
        if filterDict.get(originKey, None):
            return filterDict[originKey]
        return originKey

    def _getXPath(self, kwargs: Dict[str, str]):

        def filter_selectors(kwargs: Dict[str, str]):
            """
            filter the selector
            """
            new_kwargs = dict()
            SPECIAL_KEY = {"mask", "childOrSibling", "childOrSiblingSelector"}
            for key, val in kwargs.items():
                if key in SPECIAL_KEY:
                    continue
                key = self._transferU2Keys(key)
                new_kwargs[key] = val
            return new_kwargs

        kwargs = filter_selectors(kwargs)

        attrLocs = [
            f"[@{k}='{v}']" for k, v in kwargs.items()
        ]
        xpath = f".//node{''.join(attrLocs)}"
        return xpath


    @property
    def exists(self):
        dict.update(self.selector, {"covered": "false"})
        xpath = self._getXPath(self.selector)
        matched_widgets = self.session.xml.xpath(xpath)
        return bool(matched_widgets)

    def __len__(self):
        xpath = self._getXPath(self.selector)
        matched_widgets = self.session.xml.xpath(xpath)
        return len(matched_widgets)
    
    def child(self, **kwargs):
        return StaticU2UiObject(self.session, self.selector.clone().child(**kwargs))
    
    def sibling(self, **kwargs):
        return StaticU2UiObject(self.session, self.selector.clone().sibling(**kwargs))


def _get_bounds(raw_bounds):
    pattern = re.compile(r"\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]")
    m = re.match(pattern, raw_bounds)
    try:
        bounds = [int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))]
    except Exception as e:
        print(f"raw_bounds: {raw_bounds}", flush=True)
        print(f"Please report this bug to Kea2", flush=True)
        raise RuntimeError(e)

    return bounds


class _HindenWidgetFilter:
    def __init__(self, root: etree._Element):
        # self.global_drawing_order = 0
        self._nodes = []

        self.idx = rtree.index.Index()
        self.set_covered_attr(root)

        # xml_bytes = etree.tostring(root, pretty_print=True, encoding="utf-8", xml_declaration=True)
        # with open("filtered_tree.xml", "wb") as f:
        #     f.write(xml_bytes)
        # xml_bytes

    def _iter_by_drawing_order(self, ele: etree._Element):
        """
        iter by drawing order (DFS)
        """
        if ele.tag == "node":
            yield ele

        children = list(ele)
        try:
            children.sort(key=lambda e: int(e.get("drawing-order", 0)))
        except (TypeError, ValueError):
            pass

        for child in children:
            yield from self._iter_by_drawing_order(child)
   
    def set_covered_attr(self, root: etree._Element):
        self._nodes: List[etree._Element] = list()
        for e in self._iter_by_drawing_order(root):
            # e.set("global-order", str(self.global_drawing_order))
            # self.global_drawing_order += 1
            e.set("covered", "false")

            # algorithm: filter by "clickable"
            clickable = (e.get("clickable", "false") == "true")
            _raw_bounds = e.get("bounds")
            if _raw_bounds is None:
                continue
            bounds = _get_bounds(_raw_bounds)
            if clickable:
                covered_widget_ids = list(self.idx.contains(bounds))
                if covered_widget_ids:
                    for covered_widget_id in covered_widget_ids:
                        node = self._nodes[covered_widget_id]
                        node.set("covered", "true")
                        self.idx.delete(
                            covered_widget_id,
                            _get_bounds(self._nodes[covered_widget_id].get("bounds"))
                        )

            cur_id = len(self._nodes)
            center = [
                (bounds[0] + bounds[2]) / 2,
                (bounds[1] + bounds[3]) / 2
            ]
            self.idx.insert(
                cur_id,
                (center[0], center[1], center[0], center[1])
            )
            self._nodes.append(e)


class U2StaticDevice(u2.Device):
    def __init__(self, script_driver):
        self.xml: etree._Element = None
        self._script_driver = script_driver

    def __call__(self, **kwargs):
        return StaticU2UiObject(session=self, selector=u2.Selector(**kwargs))

    @property
    def xpath(self) -> u2.xpath.XPathEntry:
        def get_page_source(self):
            # print("[Debug] Using static get_page_source method")
            return u2.xpath.PageSource.parse(self._d.xml_raw)
        xpathEntry = _XPathEntry(self)
        xpathEntry.get_page_source = types.MethodType(
            get_page_source, xpathEntry
        )
        return xpathEntry
    
    def __getattr__(self, attr):
        """Proxy other methods to script_driver"""
        logger.debug(f"{attr} not exists in static checker, proxy to script_driver.")
        return getattr(self._script_driver, attr)

class _XPathEntry(u2.xpath.XPathEntry):
    def __init__(self, d):
        self.xpath = None
        super().__init__(d)
        
    def __call__(self, xpath, source = None):
        # TODO fully support xpath in widget.block.py
        self.xpath = xpath
        return super().__call__(xpath, source)


class U2StaticChecker(AbstractStaticChecker):
    """
    This is the StaticChecker used to check the precondition.
    We use the static checker due to the performing issues when runing multi-properties.
    
    *e.g. the following self.d use U2StaticChecker*
    ```
    @precondition(lambda self: self.d("battery").exists)
    def test_battery(self):
        ...
    ```
    """
    def __init__(self):
        self.d = U2StaticDevice(U2ScriptDriver().getInstance()) 

    def setHierarchy(self, hierarchy: str):
        if hierarchy is None:
            return
        self.d.xml = etree.fromstring(hierarchy.encode("utf-8"))
        _HindenWidgetFilter(self.d.xml)

    def getInstance(self, hierarchy: str=None):
        self.setHierarchy(hierarchy)
        return self.d


"""
The definition of U2Driver
"""
class U2Driver(AbstractDriver):
    scriptDriver = None
    staticChecker = None

    @classmethod
    def setDeviceSerial(cls, deviceSerial):
        U2ScriptDriver.setDeviceSerial(deviceSerial)

    @classmethod
    def getScriptDriver(self):
        if self.scriptDriver is None:
            self.scriptDriver = U2ScriptDriver()
        return self.scriptDriver.getInstance()

    @classmethod
    def getStaticChecker(self, hierarchy=None):
        if self.staticChecker is None:
            self.staticChecker = U2StaticChecker()
        return self.staticChecker.getInstance(hierarchy)

    @classmethod
    def tearDown(self):
        self.scriptDriver.tearDown()


"""
Other Utils
"""
def forward_port(self, remote: Union[int, str]) -> int:
        """forward remote port to local random port"""
        remote = 8090
        if isinstance(remote, int):
            remote = "tcp:" + str(remote)
        for f in self.forward_list():
            if (
                f.serial == self._serial
                and f.remote == remote
                and f.local.startswith("tcp:")
            ):  # yapf: disable
                return int(f.local[len("tcp:") :])
        local_port = get_free_port()
        self.forward("tcp:" + str(local_port), remote)
        logger.debug(f"forwading port: tcp:{local_port} -> {remote}")
        return local_port


def selector_to_xpath(selector: u2.Selector, is_initial: bool = True) -> str:
    """
    Convert a u2 Selector into an XPath expression compatible with Java Android UI controls.

    Args:
        selector (u2.Selector): A u2 Selector object
        is_initial (bool): Whether it is the initial node, defaults to True

    Returns:
        str: The corresponding XPath expression
    """
    try:
        if is_initial:
            xpath = ".//node"
        else:
            xpath = "node"

        conditions = []

        if "className" in selector:
            conditions.insert(0, f"[@class='{selector['className']}']")  # 将 className 条件放在前面

        if "text" in selector:
            conditions.append(f"[@text='{selector['text']}']")
        elif "textContains" in selector:
            conditions.append(f"[contains(@text, '{selector['textContains']}')]")
        elif "textMatches" in selector:
            conditions.append(f"[re:match(@text, '{selector['textMatches']}')]")
        elif "textStartsWith" in selector:
            conditions.append(f"[starts-with(@text, '{selector['textStartsWith']}')]")

        if "description" in selector:
            conditions.append(f"[@content-desc='{selector['description']}']")
        elif "descriptionContains" in selector:
            conditions.append(f"[contains(@content-desc, '{selector['descriptionContains']}')]")
        elif "descriptionMatches" in selector:
            conditions.append(f"[re:match(@content-desc, '{selector['descriptionMatches']}')]")
        elif "descriptionStartsWith" in selector:
            conditions.append(f"[starts-with(@content-desc, '{selector['descriptionStartsWith']}')]")

        if "packageName" in selector:
            conditions.append(f"[@package='{selector['packageName']}']")
        elif "packageNameMatches" in selector:
            conditions.append(f"[re:match(@package, '{selector['packageNameMatches']}')]")

        if "resourceId" in selector:
            conditions.append(f"[@resource-id='{selector['resourceId']}']")
        elif "resourceIdMatches" in selector:
            conditions.append(f"[re:match(@resource-id, '{selector['resourceIdMatches']}')]")

        bool_props = [
            "checkable", "checked", "clickable", "longClickable", "scrollable",
            "enabled", "focusable", "focused", "selected", "covered"
        ]
        for prop in bool_props:
            if prop in selector:
                value = "true" if selector[prop] else "false"
                conditions.append(f"[@{prop}='{value}']")

        if "index" in selector:
            conditions.append(f"[@index='{selector['index']}']")
        elif "instance" in selector:
            conditions.append(f"[@instance='{selector['instance']}']")

        xpath += "".join(conditions)

        if "childOrSibling" in selector and selector["childOrSibling"]:
            for i, relation in enumerate(selector["childOrSibling"]):
                sub_selector = selector["childOrSiblingSelector"][i]
                sub_xpath = selector_to_xpath(sub_selector, False)  # 递归处理子选择器

                if relation == "child":
                    xpath += f"/{sub_xpath}"
                elif relation == "sibling":
                    xpath_initial = xpath
                    xpath = '(' + xpath_initial + f"/following-sibling::{sub_xpath} | " + xpath_initial + f"/preceding-sibling::{sub_xpath})"

        return xpath

    except Exception as e:
        print(f"Error occurred during selector conversion: {e}")
        return "//error"

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def get_free_port():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 0))
        try:
            return s.getsockname()[1]
        finally:
            s.close()
    except OSError:
        # bind 0 will fail on Manjaro, fallback to random port
        # https://github.com/openatx/adbutils/issues/85
        for _ in range(20):
            port = random.randint(10000, 20000)
            if not is_port_in_use(port):
                return port
        raise RuntimeError("No free port found")
