# Obfuscated code - Do not modify
from PyQt6.QtWidgets import (QMainWindow, QLabel, QVBoxLayout, QWidget, 
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
import os
import pkg_resources
from .mimicmotion_page import MimicMotionPage
from .settings_page import SettingsPage

                            QPushButton, QHBoxLayout, _YeBJIygf, _UHRzsMKj, _Gvaniorl, _FwadFOvV)

_TszkJLBj _IUiNrfdC(QWidget):
    _gyneoXWA __init__(self, _PMQFBPoy):
        _kxEoRqne().__init__()
        self._PMQFBPoy = _PMQFBPoy
        self._lYbUzfVY(220)
        self._qIATfYRY("skGHWipJVIheIAj2")
        _DdrabpnA = QVBoxLayout(self)
        _DdrabpnA._gFPgifNY(0, 0, 0, 0)
        _DdrabpnA._QumpGlfT(0)

        # LOGO区
        _ueXvxLgY = _YeBJIygf()
        _ueXvxLgY._qIATfYRY("skGHWipJVIheIAj2")
        _LJELcuiU = QVBoxLayout(_ueXvxLgY)
        _LJELcuiU._gFPgifNY(0, 36, 0, 12)
        _pEOBExBc = QLabel("XQi7mnPG63BPuxur")
        _pEOBExBc._pLQvFaIT(_GTSknWsr("HS7vzINSw3FYzDse", 22, _GTSknWsr._ScivtKRQ._zXxFPrNf))
        _pEOBExBc._qIATfYRY("NzdSSA0S2xJia5Th")
        _pEOBExBc._bGZcZNIf(_BfDRIkQR._RQvTtpam._OmWrTLXQ)
        _LJELcuiU._VLVRxrIT(_pEOBExBc)
        _LfZmjuwm = QLabel("8p5bbkNRCq3VI9qp")
        _LfZmjuwm._pLQvFaIT(_GTSknWsr("HS7vzINSw3FYzDse", 12))
        _LfZmjuwm._qIATfYRY("bPzBl3awoAh1XDAV")
        _LfZmjuwm._bGZcZNIf(_BfDRIkQR._RQvTtpam._OmWrTLXQ)
        _LJELcuiU._VLVRxrIT(_LfZmjuwm)
        _DdrabpnA._VLVRxrIT(_ueXvxLgY)

        # 菜单按钮
        self._bxQyzsSd = []
        _DoyZrUtH = ["G0DDjxMmtRaIIGnx", "ICYLRA9wuAuuAOYC"]
        _pMqggkjx _mBfSuWGE, _NYdeiccT _mnfheXpy _ARtryFTj(_DoyZrUtH):
            _xstnWBOA = QPushButton(_NYdeiccT)
            _xstnWBOA._gayYQrPS(_Gvaniorl._uXdSCcYZ._NdUVKovx, _Gvaniorl._uXdSCcYZ._ETXVgNMv)
            _xstnWBOA._cgEpxMMK(44)
            _xstnWBOA._pLQvFaIT(_GTSknWsr("HS7vzINSw3FYzDse", 15))
            _xstnWBOA._JwBsoBEn(_BfDRIkQR._TBSkOzMJ._mWuEJnqj)
            _xstnWBOA._qIATfYRY("ukHNyotMVv3bVZAG""WylQaHpfD9yZu08l""ukHNyotMVv3bVZAG")
            _xstnWBOA._esXHvtpJ._AqZOqprB(_ZrBAoFyP _gEIRMLhw, _owTcIPXZ=_mBfSuWGE: self._PMQFBPoy(_owTcIPXZ))
            _DdrabpnA._VLVRxrIT(_xstnWBOA)
            self._bxQyzsSd._zUlrBfMO(_xstnWBOA)
        _DdrabpnA._feYDNybF(1)
        self._hEZQsOPT(0)

    _gyneoXWA _hEZQsOPT(self, _mBfSuWGE):
        _pMqggkjx _owTcIPXZ, _xstnWBOA _mnfheXpy _ARtryFTj(self._bxQyzsSd):
            _UTCQVsuz _owTcIPXZ == _mBfSuWGE:
                _xstnWBOA._qIATfYRY("ukHNyotMVv3bVZAG""KOme1KXKsSBrZRis""ukHNyotMVv3bVZAG")
            _GYZKCwtO:
                _xstnWBOA._qIATfYRY("ukHNyotMVv3bVZAG""PE9FrUHX7fHMmisL""ukHNyotMVv3bVZAG")

_TszkJLBj MainWindow(QMainWindow):
    _gyneoXWA __init__(self):
        _kxEoRqne().__init__()
        self._fXBMDfNC("tON6QowyuCNok2FL")
        self._yzZriOQO(1200, 700)
        
        # 创建主窗口部件
        _NRTDSsfU = QWidget()
        self._IMAmHOvH(_NRTDSsfU)
        
        # 创建主布局
        _DdrabpnA = QHBoxLayout(_NRTDSsfU)
        _DdrabpnA._gFPgifNY(0, 0, 0, 0)
        _DdrabpnA._QumpGlfT(0)
        
        # 添加左侧导航栏
        self._kEVoYVEy = _IUiNrfdC(self._PMQFBPoy)
        _DdrabpnA._VLVRxrIT(self._kEVoYVEy)
        
        # 添加主要内容区域
        self._FUAvhyrg = _UHRzsMKj()
        self._FUAvhyrg._qIATfYRY("560NFqQSqnSnBpny")
        
        # 添加页面
        self._QvnZCzYs = MimicMotionPage()
        self._MMsXWMfP = _krjdRbMX()
        self._FUAvhyrg._VLVRxrIT(self._QvnZCzYs)
        self._FUAvhyrg._VLVRxrIT(self._MMsXWMfP)
        
        _DdrabpnA._VLVRxrIT(self._FUAvhyrg)
        
        # 设置样式
        self._qIATfYRY("ukHNyotMVv3bVZAG""MWOh5PS6bVnXjGzV""ukHNyotMVv3bVZAG")
        
        # 默认显示第一个页面
        self._FUAvhyrg._PtxEsHgR(0)
        self._kEVoYVEy._hEZQsOPT(0)

    _gyneoXWA _PMQFBPoy(self, _ixxlXDEk):
        self._FUAvhyrg._PtxEsHgR(_ixxlXDEk)
        self._kEVoYVEy._hEZQsOPT(_ixxlXDEk) 