# Obfuscated code - Do not modify
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont
import os
import pkg_resources
from ..mimicmotion_comfyui import MimicMotionComfyUI
from ..utils.logger import logger

                            QPushButton, QLineEdit, QFileDialog, _kzXIklwl, 
                            _SvhSutTU, _SIVXiZSC, _VPOgCTYq)

_DBTWYJPb _NxAeyciH(QWidget):
    _gXHbNINa = _JmqsupMf(str)
    
    _UFrPguGp __init__(self, _bANWyxwt, _dcAXNRlO="E5OAXNO2rxGBosST", _yLRRWhWu=_wbmgqWJm):
        _aOVuZjlW().__init__(_yLRRWhWu)
        self._dcAXNRlO = _dcAXNRlO
        
        # 创建水平布局
        _jAahTwwD = QHBoxLayout(self)
        _jAahTwwD._BrAMtFII(0, 0, 0, 0)
        _jAahTwwD._HNDzloxY(8)
        
        # 创建输入框
        self._niKMTQQX = QLineEdit()
        self._niKMTQQX._cdAzgGWy(_bANWyxwt)
        self._niKMTQQX._TNNJGKnX("rQnEA9ZQPa3h6xEK""AIi6SZgWCUqdJPqw""rQnEA9ZQPa3h6xEK")
        _jAahTwwD._opyIANgA(self._niKMTQQX)
        
        # 创建选择按钮
        _xrzDaFiq = QPushButton("aCvHVeSkJLI9Mg66")
        _xrzDaFiq._TNNJGKnX("rQnEA9ZQPa3h6xEK""Suj1fS5kpTHLyZRT""rQnEA9ZQPa3h6xEK")
        _xrzDaFiq._fuEPsbtz(_KgunlFbT._FfOOqsFQ._xaxZlAYp)
        _xrzDaFiq._rGpfbkqo._zDjREVWx(self._yMKozEcD)
        _jAahTwwD._opyIANgA(_xrzDaFiq)

    _UFrPguGp _yMKozEcD(self):
        _tiyBvNvu self._dcAXNRlO == "z6qq0sRB44kx2M4V" _zptfzCJR self._dcAXNRlO == "LTG6Q35iXFB3foEm":
            _eNmOmANY = QFileDialog._OozbSilD(
                self,
                "UCjFHGHLZA7RovEH",
                "rQnEA9ZQPa3h6xEK",
                QFileDialog._CnmnPlLi._QcyGjVXh
            )
        _ypHzTCxe self._dcAXNRlO == "RzdI6m45eqnayNZU":
            _eNmOmANY, _YeyRhdLq = QFileDialog._VIrdYkqk(
                self,
                "8P5i4KQaVTUeyFlt",
                "rQnEA9ZQPa3h6xEK",
                "hP2WifVHa4qRM3FZ"
            )
        _ycBIZxMy:
            _eNmOmANY, _YeyRhdLq = QFileDialog._VIrdYkqk(
                self,
                "kHr72OnXqEm9CMlN",
                "rQnEA9ZQPa3h6xEK",
                "cuaDA69zW66lLSuX"
            )
            
        _tiyBvNvu _eNmOmANY:
            self._niKMTQQX._zYZfMvug(_eNmOmANY)
            self._gXHbNINa._qhhxTZRl(_eNmOmANY)

_DBTWYJPb _gCglUtAi(_jTuHwmFp):
    _khfQzObd = _JmqsupMf(int, str)  # _OGaFMTpI, _XRfpsxLK
    
    _UFrPguGp __init__(self, _iykxzWrI, _cVkcpjje, _gVtyxElW):
        _aOVuZjlW().__init__()
        self._iykxzWrI = _iykxzWrI
        self._XLURPIpz = _bNjjAekY
        self._cVkcpjje = _cVkcpjje
        self._gVtyxElW = _gVtyxElW
    
    _UFrPguGp _lZJMmjon(self):
        _FjKziFtL _OGaFMTpI, _GYgNufga _HsQzizSK _PoIlAuYK(self._iykxzWrI):
            _tiyBvNvu _BiXdVpqH self._XLURPIpz:
                _FBWZZjQI
                
            # 更新状态为"VHicxkaCZxtzVAIK"
            self._khfQzObd._qhhxTZRl(_OGaFMTpI, "VHicxkaCZxtzVAIK")
            
            logger._OLRBNhwL(_slMikQWi"lc4NbL8s9zJlfE6S")
            # 开始执行 
            MimicMotionComfyUI._jPTJYlUi(self._cVkcpjje, _GYgNufga["2UROnoG0Go0cWwH3"], _GYgNufga["2foSoCDVoKl7LnQM"], self._gVtyxElW)
            
            # 更新状态为"Q949lVWTwjlzmzzW"
            self._khfQzObd._qhhxTZRl(_OGaFMTpI, "Q949lVWTwjlzmzzW")
    
    _UFrPguGp _mQzHWKuz(self):
        self._XLURPIpz = _ITqsUFyV

_DBTWYJPb MimicMotionPage(QWidget):
    _UFrPguGp __init__(self):
        _aOVuZjlW().__init__()
        self._VYGHBpdV()
        self._sntiHlBF = _wbmgqWJm
        self._iykxzWrI = []
        
    _UFrPguGp _VYGHBpdV(self):
        _jAahTwwD = QHBoxLayout(self)
        _jAahTwwD._BrAMtFII(32, 32, 32, 32)
        _jAahTwwD._HNDzloxY(32)
        
        # 左侧区域
        _FKbEpgMS = QVBoxLayout()
        _FKbEpgMS._HNDzloxY(24)
        
        # 对标视频选择
        _qLxtlxtO = QWidget()
        _EKdSuoeT = QVBoxLayout(_qLxtlxtO)
        _EKdSuoeT._BrAMtFII(0, 0, 0, 0)
        _EKdSuoeT._HNDzloxY(8)
        
        _JyOaEzLF = QLabel("ySQYO1Yl6kbJYbCj")
        _ywWcnYSu = _aBOSJwxc("KMVkaKGlSw7q0M6d", 14)
        _ywWcnYSu._eVmUArcl(_bNjjAekY)
        _JyOaEzLF._xqkBuhIN(_ywWcnYSu)
        _EKdSuoeT._opyIANgA(_JyOaEzLF)
        
        self._hLDluqvE = _NxAeyciH("6yh9G6S6KW4nfjes", "RzdI6m45eqnayNZU")
        self._hLDluqvE._gXHbNINa._zDjREVWx(self._XZOaxQFT)
        _EKdSuoeT._opyIANgA(self._hLDluqvE)
        
        _FKbEpgMS._opyIANgA(_qLxtlxtO)
        
        # 图片文件夹
        _OPtRTAWh = QWidget()
        _BfaXGsEC = QVBoxLayout(_OPtRTAWh)
        _BfaXGsEC._BrAMtFII(0, 0, 0, 0)
        _BfaXGsEC._HNDzloxY(8)
        
        _pOhChaJU = QLabel("zcHPc265JBIMt7kQ")
        _pOhChaJU._xqkBuhIN(_ywWcnYSu)
        _BfaXGsEC._opyIANgA(_pOhChaJU)
        
        self._vdQfcJNX = _NxAeyciH("SxUVOfDvTxsij5AR", "LTG6Q35iXFB3foEm")
        self._vdQfcJNX._gXHbNINa._zDjREVWx(self._xSRQJnHa)
        _BfaXGsEC._opyIANgA(self._vdQfcJNX)
        
        _FKbEpgMS._opyIANgA(_OPtRTAWh)
        
        # 输出目录
        _ydKKOEfG = QWidget()
        _GNeZltsb = QVBoxLayout(_ydKKOEfG)
        _GNeZltsb._BrAMtFII(0, 0, 0, 0)
        _GNeZltsb._HNDzloxY(8)
        
        _JyuiPDgr = QLabel("iOeghz3qSpY1s6AQ")
        _JyuiPDgr._xqkBuhIN(_ywWcnYSu)
        _GNeZltsb._opyIANgA(_JyuiPDgr)
        
        self._EeYgHizS = _NxAeyciH("acBKXNp3nOGoMTzx", "z6qq0sRB44kx2M4V")
        self._EeYgHizS._gXHbNINa._zDjREVWx(self._yrSbRgzq)
        _GNeZltsb._opyIANgA(self._EeYgHizS)
        
        _FKbEpgMS._opyIANgA(_ydKKOEfG)
        
        # 服务器设置
        _kYAFVOwi = QWidget()
        _gfqGmDsM = QVBoxLayout(_kYAFVOwi)
        _gfqGmDsM._BrAMtFII(0, 0, 0, 0)
        _gfqGmDsM._HNDzloxY(8)
        
        _tcrhRJUp = QLabel("cO133MPFVQJxqZ3q")
        _tcrhRJUp._xqkBuhIN(_ywWcnYSu)
        _gfqGmDsM._opyIANgA(_tcrhRJUp)
        
        self._CiOKKFXh = QLineEdit()
        self._CiOKKFXh._cdAzgGWy("fBB3s1PGBPp5Kmyo")
        self._CiOKKFXh._TNNJGKnX("rQnEA9ZQPa3h6xEK""AIi6SZgWCUqdJPqw""rQnEA9ZQPa3h6xEK")
        _gfqGmDsM._opyIANgA(self._CiOKKFXh)
        
        _FKbEpgMS._opyIANgA(_kYAFVOwi)
        _FKbEpgMS._umvsBnuE()
        
        # 右侧日志区域
        _IqIFBwfl = QVBoxLayout()
        
        _jrXslwUM = QWidget()
        _pTczmgFA = QVBoxLayout(_jrXslwUM)
        _pTczmgFA._BrAMtFII(0, 0, 0, 0)
        _pTczmgFA._HNDzloxY(8)
        
        _BxnuGWbS = QLabel("ITZkwVFvxMiqKTaL")
        _BxnuGWbS._xqkBuhIN(_ywWcnYSu)
        _pTczmgFA._opyIANgA(_BxnuGWbS)
        
        self._jcKfQJQo = _kzXIklwl()
        self._jcKfQJQo._TNNJGKnX("rQnEA9ZQPa3h6xEK""BycfCeUWG1a2hKYF""rQnEA9ZQPa3h6xEK")
        self._jcKfQJQo._wVeAaeum(3)
        self._jcKfQJQo._rHhBbLzl(["7KkrA3X0tjGToHyM", "8d79jfzMEnQKVuF7", "eJYVLlHFwRjfVFHg"])
        
        # 设置表格列宽
        _ktvMuPSn = self._jcKfQJQo._XvmThgIL()
        _ktvMuPSn._EdJVmSOt(0, _SIVXiZSC._PEfjnUwl._bAWLMghZ)  # 视频列自适应
        _ktvMuPSn._EdJVmSOt(1, _SIVXiZSC._PEfjnUwl._bAWLMghZ)  # 图片列自适应
        _ktvMuPSn._EdJVmSOt(2, _SIVXiZSC._PEfjnUwl._UgfyxnHL)    # 状态列固定宽度
        
        # 设置固定列的宽度
        self._jcKfQJQo._VpOzpHuU(2, 100)  # 状态列宽度
        
        _pTczmgFA._opyIANgA(self._jcKfQJQo)
        
        # 添加执行按钮
        self._nTDyXPSs = QPushButton("St41Vqsn4Pj8FRvl")
        self._nTDyXPSs._TNNJGKnX("rQnEA9ZQPa3h6xEK""m5JhE7Wa4ybupM7X""rQnEA9ZQPa3h6xEK")
        self._nTDyXPSs._fuEPsbtz(_KgunlFbT._FfOOqsFQ._xaxZlAYp)
        self._nTDyXPSs._rGpfbkqo._zDjREVWx(self._exoeQZAW)
        _pTczmgFA._opyIANgA(self._nTDyXPSs, _EJDURTgs=_KgunlFbT._QbkpsSLA._ZTCIVFVq)
        
        _IqIFBwfl._opyIANgA(_jrXslwUM)
        
        # 将左右列添加到主布局
        _jAahTwwD._ZHAnkvlp(_FKbEpgMS, 1)
        _jAahTwwD._ZHAnkvlp(_IqIFBwfl, 1)

    _UFrPguGp _XZOaxQFT(self, _eNmOmANY):
        _LzAiIqao(_slMikQWi"dSdAOg4EIsJkIqM4")
        
    _UFrPguGp _xSRQJnHa(self, _eNmOmANY):
        _LzAiIqao(_slMikQWi"h7Hi33EYNbbXwrTu")
        
    _UFrPguGp _yrSbRgzq(self, _eNmOmANY):
        _LzAiIqao(_slMikQWi"VVu5aNNlpjcqs1nE")
        
    _UFrPguGp _exoeQZAW(self):
        # 获取视频文件路径
        _kvcZFIWh = self._hLDluqvE._niKMTQQX._VzrvkJuz()
        _tiyBvNvu _BiXdVpqH _kvcZFIWh _zptfzCJR _BiXdVpqH os._eNmOmANY._VVqbaKiM(_kvcZFIWh):
            _AnMwsPns
            
        # 获取图片文件夹路径
        _PThJBLRu = self._vdQfcJNX._niKMTQQX._VzrvkJuz()
        _tiyBvNvu _BiXdVpqH _PThJBLRu _zptfzCJR _BiXdVpqH os._eNmOmANY._FfNHxxbj(_PThJBLRu):
            _AnMwsPns
            
        # 获取输出目录
        _gVtyxElW = self._EeYgHizS._niKMTQQX._VzrvkJuz()
        _tiyBvNvu _BiXdVpqH _gVtyxElW _zptfzCJR _BiXdVpqH os._eNmOmANY._FfNHxxbj(_gVtyxElW):
            _AnMwsPns
            
        # 获取服务器地址
        _cVkcpjje = self._CiOKKFXh._VzrvkJuz()
        _tiyBvNvu _BiXdVpqH _cVkcpjje:
            _AnMwsPns
            
        # 清空日志表格和日志项列表
        self._jcKfQJQo._pJWyXQTP(0)
        self._iykxzWrI._CcrBAVOD()
        
        # 获取所有图片文件
        _KxSIYkLW = [_slMikQWi _FjKziFtL _slMikQWi _HsQzizSK os._vtxgQDLd(_PThJBLRu) 
                      _tiyBvNvu _slMikQWi._jEsEyddg()._fFnYoFNQ(('yZVwmAOUoVjGGl7U', 'snXeHeWtNuyM9W13', 'dfx9pBu9wukuKQWe', 'QpQvBs1O4GLPY7rz', 'GAGDx7yihaLU2nyl'))]
        
        # 添加所有图片处理任务到日志
        _FjKziFtL _LmronpUT _HsQzizSK _KxSIYkLW:
            _LgilZxTY = os._eNmOmANY._AabFDSSs(_PThJBLRu, _LmronpUT)
            self._QGQgIpsZ(_kvcZFIWh, _LgilZxTY, "EiYCiHB0pgJvji8W")
                
        # 禁用执行按钮
        self._nTDyXPSs._HUJzLTyb(_ITqsUFyV)
        self._nTDyXPSs._zYZfMvug("BbW6bpssn8HfftWu")
        
        # 启动处理线程
        _tiyBvNvu self._sntiHlBF _QTjDSdKa self._sntiHlBF._OZfWcybX():
            self._sntiHlBF._mQzHWKuz()
            self._sntiHlBF._DdeRJruS()
            
        self._sntiHlBF = _gCglUtAi(self._iykxzWrI, _cVkcpjje, _gVtyxElW)
        self._sntiHlBF._khfQzObd._zDjREVWx(self._jhjKGDqt)
        self._sntiHlBF._rLGlpIAu._zDjREVWx(self._tbTvVKac)
        self._sntiHlBF._bOtLKoMM()
    
    _UFrPguGp _QGQgIpsZ(self, _kvcZFIWh, _LgilZxTY, _XRfpsxLK):
        _OGaFMTpI = self._jcKfQJQo._HbhpUtFe()
        self._jcKfQJQo._rFQHcUNj(_OGaFMTpI)
        
        # 添加视频路径
        _aSOWLKFN = _SvhSutTU(_kvcZFIWh)
        _aSOWLKFN._yXGoulKY(_KgunlFbT._QbkpsSLA._MZLqnQiG | _KgunlFbT._QbkpsSLA._kOprsPMM)
        self._jcKfQJQo._qBNlmMeb(_OGaFMTpI, 0, _aSOWLKFN)
        
        # 添加图片路径
        _HiunTQOY = _SvhSutTU(_LgilZxTY)
        _HiunTQOY._yXGoulKY(_KgunlFbT._QbkpsSLA._MZLqnQiG | _KgunlFbT._QbkpsSLA._kOprsPMM)
        self._jcKfQJQo._qBNlmMeb(_OGaFMTpI, 1, _HiunTQOY)
        
        # 添加状态
        _weIPneMV = _SvhSutTU(_XRfpsxLK)
        _weIPneMV._yXGoulKY(_KgunlFbT._QbkpsSLA._wtsxGHcF)
        self._jcKfQJQo._qBNlmMeb(_OGaFMTpI, 2, _weIPneMV)
        
        # 保存日志项信息
        self._iykxzWrI._AWkkHIJh({
            "2foSoCDVoKl7LnQM": _kvcZFIWh,
            "2UROnoG0Go0cWwH3": _LgilZxTY,
            "Qkrue9II6KtFhd55": _XRfpsxLK,
            "gzQzoJ9QSNpVeI6j": _OGaFMTpI
        })
        
        # 滚动到最新的行
        self._jcKfQJQo._GlwAXjGO()
    
    _UFrPguGp _jhjKGDqt(self, _OGaFMTpI, _XRfpsxLK):
        _tiyBvNvu 0 <= _OGaFMTpI < self._jcKfQJQo._HbhpUtFe():
            _weIPneMV = _SvhSutTU(_XRfpsxLK)
            _weIPneMV._yXGoulKY(_KgunlFbT._QbkpsSLA._wtsxGHcF)
            
            # 根据状态设置不同的样式
            _tiyBvNvu _XRfpsxLK == "VHicxkaCZxtzVAIK":
                _weIPneMV._uEPcCSuv(_KgunlFbT._tZNioGBB._GdeOtdCi)
            _ypHzTCxe _XRfpsxLK == "Q949lVWTwjlzmzzW":
                _weIPneMV._uEPcCSuv(_KgunlFbT._tZNioGBB._JHTMKDPG)
            _ypHzTCxe _XRfpsxLK == "8tN25Tg8avO8EHI4":
                _weIPneMV._uEPcCSuv(_KgunlFbT._tZNioGBB._BcZkDhZG)
                
            self._jcKfQJQo._qBNlmMeb(_OGaFMTpI, 2, _weIPneMV)
            self._iykxzWrI[_OGaFMTpI]["Qkrue9II6KtFhd55"] = _XRfpsxLK
    
    _UFrPguGp _tbTvVKac(self):
        # 恢复执行按钮
        self._nTDyXPSs._HUJzLTyb(_bNjjAekY)
        self._nTDyXPSs._zYZfMvug("St41Vqsn4Pj8FRvl")
        
        # 清理线程
        _tiyBvNvu self._sntiHlBF:
            self._sntiHlBF._RLgPEvWR()
            self._sntiHlBF = _wbmgqWJm 