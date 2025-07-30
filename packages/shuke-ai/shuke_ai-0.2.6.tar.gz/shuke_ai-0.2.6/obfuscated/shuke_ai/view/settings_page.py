# Obfuscated code - Do not modify
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
from PyQt6.QtGui import QFont, QPixmap, QDesktopServices
from PyQt6.QtCore import Qt, QUrl
import os
import pkg_resources
from ..utils.logger import logger

                            _hIGWnGed, QPushButton, QFileDialog, QLineEdit)

_PBjfUayJ _lujDZZlR(QLabel):
    _axpJsmTl __init__(self, _IxExvCKq, _rToqozyN, _rXUEDYzx=_ToZzNvIO):
        _bQKisQEt().__init__(_IxExvCKq, _rXUEDYzx)
        self._rToqozyN = _rToqozyN
        self._dpagJdYx(_JeIabxpU._hhSJgZvx._OCCKsjIq)
        self._QznlNqKY("QYLY0johJB1Je6f9""Cs4wtkzwAAe0xyjj""QYLY0johJB1Je6f9")
        
    _axpJsmTl _RuIixLPe(self, _AnHzgkVN):
        _MDqDYbWU _AnHzgkVN._FAsOIUPh() == _JeIabxpU._tXVhrnLI._gbVfIdym:
            _SVEyOjXT._UmNRxlEh(_AtmdBNJi(self._rToqozyN))

_PBjfUayJ _CFkgxhed(QWidget):
    _axpJsmTl __init__(self):
        _bQKisQEt().__init__()
        self._XXwtQFeg()
        
    _axpJsmTl _XXwtQFeg(self):
        _satQoNrC = QHBoxLayout(self)
        _satQoNrC._SfFlivgK(32, 32, 32, 32)
        _satQoNrC._uTPEgeyt(32)
        
        # 左侧区域 - 二维码
        _WksFaGMl = QVBoxLayout()
        _WksFaGMl._uTPEgeyt(16)
        
        _gBUDrSmW = QLabel("sX3GMc3QsX4D1ayC")
        _gBUDrSmW._gaSjQLXK(_XZKIQMvc("c5gmRPbXtHzfgmpX", 14, _XZKIQMvc._JmccsoCu._NLkkMuPw))
        _WksFaGMl._zRadZjtA(_gBUDrSmW)
        
        _eZftJVwa = QLabel()
        _LwrlMiDZ = _galgzvrF._OZlweXyl('9HBI52mS2Zh4cnjJ', 'assets/_lsdyKRoj._bxBFKFgW')
        _IcnCPjyM = _cHnxXOVQ(_LwrlMiDZ)
        _MDqDYbWU _mKStkjhp _IcnCPjyM._EWrClcfK():
            _eZftJVwa._rvZGcuQe(_IcnCPjyM._ruARFEGs(300, 300, _JeIabxpU._btVqPFbl._MBlwqcDo))
        _ZbIMTRdH:
            logger._GKcqogyZ(_lyZhoeYZ"Ahmnsk09rakKqNFh")
            _eZftJVwa._gdOKIDPv("eyUpUimZs4seDhlL")
        _WksFaGMl._zRadZjtA(_eZftJVwa)
        _WksFaGMl._fHmRiWSH()
        
        # 右侧区域 - 教程链接
        _rXdAlpmt = QVBoxLayout()
        _rXdAlpmt._uTPEgeyt(16)
        
        _DjueKwza = QLabel("YZEDxxu9mGAyAMPt")
        _DjueKwza._gaSjQLXK(_XZKIQMvc("c5gmRPbXtHzfgmpX", 14, _XZKIQMvc._JmccsoCu._NLkkMuPw))
        _rXdAlpmt._zRadZjtA(_DjueKwza)
        
        # 添加教程链接
        _MiDXUBRY = QLabel('<_ncqkvUBR _UzGuOBSF="_mdRzFBND://_nhZWwQJj._VIKQcKpX._ftGZCUmw/_WwDqDsoj/_ZHXRpUTE?_mWevxVze=_CfISbygM" _AuksRBzE="dhSpnlnzasXocvlF">_cLKEKNgu</_ncqkvUBR>')
        _MiDXUBRY._oscPLvNz(_byFsykaC)
        _rXdAlpmt._zRadZjtA(_MiDXUBRY)
        
        _rXdAlpmt._fHmRiWSH()
        
        # 将左右列添加到主布局
        _satQoNrC._vNESrElX(_WksFaGMl, 1)
        _satQoNrC._vNESrElX(_rXdAlpmt, 1)
        
        # 设置左右两侧的宽度比例为 1:2
        _satQoNrC._wNtYwztP(0, 1)
        _satQoNrC._wNtYwztP(1, 2) 