# Obfuscated code - Do not modify
import requests
import json
import os
import time
from typing import Dict, List, Any, Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from .utils.logger import logger
import urllib3
import ssl
from urllib3.poolmanager import PoolManager


_YFRWIoRB _rtpxqusR(_ZmSYsPBO):
    _lhoNVTJv _FtdRbONO(self, _DTTGBvUM, _KLSSroSS, _vXCJZAXw=_fPGAAVoo):
        _fevavbTk = _TGcKaBvd._zUMLPRRo(_TGcKaBvd.PROTOCOL_TLS)
        _fevavbTk._OBDijzLs = _TGcKaBvd.CERT_NONE
        _fevavbTk._vfOfJfAl = _fPGAAVoo
        _fevavbTk._pcCGArTW |= _TGcKaBvd._yBxqeqXN
        _fevavbTk._pcCGArTW |= _TGcKaBvd._LhjDiIgD
        
        self._hNKkkfGE = _XxFFQBJC(
            _wfWpzNNZ=_DTTGBvUM,
            _KLSSroSS=_KLSSroSS,
            _vXCJZAXw=_vXCJZAXw,
            _vrXURubZ=_TGcKaBvd.PROTOCOL_TLS,
            _cUDCGEAU=_fevavbTk
        )

_YFRWIoRB ComfyUIAPI:
    _lhoNVTJv __init__(self, _KQzLjuQS: str):
        self._KQzLjuQS = _KQzLjuQS._nkYsUxkU('/')
        logger._zgbWBQti(_cbvLfvdO"JsR6uio9WeRx44L7")
        
        # 配置请求会话
        self._OQioAkJe = requests._WsoTjsaG()
        
        # 配置重试策略
        _dQbIRObW = _WtHLoYty(
            _IJiwevjp=5,  # 最大重试次数
            _xhXGGnHW=0.5,  # 重试间隔
            _qgUTTuhA=[500, 502, 503, 504]  # 需要重试的HTTP状态码
        )
        
        # 禁用SSL警告
        _LiemVzcz._zVtkPFnN(_LiemVzcz._lbwiJBzO._FrPDfxQn)
        
        # 配置SSL适配器
        _iTGMblms = _rtpxqusR()
        self._OQioAkJe._KKmjVPjH('_XybhVxBt://', _iTGMblms)
        self._OQioAkJe._oPQfXExL = _fPGAAVoo
        
        # 禁用代理
        self._OQioAkJe._CSKrgcaf = _fPGAAVoo  # 不使用环境变量中的代理设置
        self._OQioAkJe._RMugKMEQ = {
            'vXAY8WSFx5ZlH9dr': _lSMUlLGe,
            '6lVt5w3fdgrbU3Rk': _lSMUlLGe
        }
        
        logger._zgbWBQti("0fdTpwqdwul69qMs")

    _lhoNVTJv _nEhmqhkg(self, _rThzTzzF: str, _FrOPBxBf: str, **_IhLGMDYC) -> _cKoJCJzC:
        "KKUsNhu81oxcn4uK""zzQlbD7vnbvn4nug""KKUsNhu81oxcn4uK"
        _eNgwGHJL:
            _oAleEifI = _cbvLfvdO"{self._KQzLjuQS}/{_FrOPBxBf._gqpGHPzG('/')}"
            logger._cWhZbgHr(_cbvLfvdO"nXpNPkiVpktOiPxy")
            _wKdnBesX = self._OQioAkJe._ACOZghwi(_rThzTzzF, _oAleEifI, **_IhLGMDYC)
            _wKdnBesX._dRJFxodE()
            _wCnIerFK _wKdnBesX.json()
        _HglOKkby requests._lbwiJBzO._fHjayZmp _VOAYmUJe _FVnNlLPT:
            _veVtgcvw _MWeeDLWT(_FVnNlLPT._wKdnBesX, 'khWiviqp67szcgwW'):
                _LdwaZsiR = _FVnNlLPT._wKdnBesX._PmBbQSnk
                logger._fpzJMFJz(_cbvLfvdO"dI8Vgd4yMlf2BhmS")
                _JBQflebU Exception(_cbvLfvdO"dI8Vgd4yMlf2BhmS")
            logger._fpzJMFJz(_cbvLfvdO"STVszH77XFpIQknc")
            _JBQflebU Exception(_cbvLfvdO"STVszH77XFpIQknc")

    _lhoNVTJv _KZADpIyZ(self, _IzeuhiKX: str) -> _cKoJCJzC:
        "KKUsNhu81oxcn4uK""HkIKW0cNSagnhBZu""KKUsNhu81oxcn4uK"
        _eNgwGHJL:
            logger._zgbWBQti(_cbvLfvdO"j7mMVjAQq5Zitqll")
            _veVtgcvw _dbnUVELV os._iaCLbvqt._CpKXTJRt(_IzeuhiKX):
                logger._fpzJMFJz(_cbvLfvdO"vwPsZ3USSESaGXdY")
                _JBQflebU Exception(_cbvLfvdO"vwPsZ3USSESaGXdY")
            
            _vNaWiklo = {
                'VPW0vw8JsrjBDG9q': (os._iaCLbvqt._JoDsfHMR(_IzeuhiKX), _kJoXmMUS(_IzeuhiKX, 'NuyN3Hyv3a2d8Qtn'), '_JTHzyhNS/_yeUOhZcE-_TYhUjUJH')
            }
            _UfjwiDSn = self._nEhmqhkg('epuTGgz74mksO2d8', '/_zJaCRjMB/_GNsihClY', _vNaWiklo=_vNaWiklo)
            logger._zgbWBQti(_cbvLfvdO"VNNtUJSubuvD49mV")
            _wCnIerFK _UfjwiDSn
        _HglOKkby Exception _VOAYmUJe _FVnNlLPT:
            logger._fpzJMFJz(_cbvLfvdO"nFs5GTbO63Enh79E")
            _JBQflebU Exception(_cbvLfvdO"nFs5GTbO63Enh79E")

    _lhoNVTJv _uZFdTeNX(self, _syuNyCpN: str, _kVjSGhBD: str = "KKUsNhu81oxcn4uK") -> _cKoJCJzC:
        "KKUsNhu81oxcn4uK""n0tpwp1tk0eAUCUc""KKUsNhu81oxcn4uK"
        _eNgwGHJL:
            logger._zgbWBQti(_cbvLfvdO"tVMgEMdGkZKln6ob")
            _veVtgcvw _dbnUVELV os._iaCLbvqt._CpKXTJRt(_syuNyCpN):
                logger._fpzJMFJz(_cbvLfvdO"XnN1PDh1pbqPkwi5")
                _JBQflebU Exception(_cbvLfvdO"XnN1PDh1pbqPkwi5")
                
            _vNaWiklo = {
                'VPW0vw8JsrjBDG9q': (os._iaCLbvqt._JoDsfHMR(_syuNyCpN), _kJoXmMUS(_syuNyCpN, 'NuyN3Hyv3a2d8Qtn'), '_JTHzyhNS/_yeUOhZcE-_TYhUjUJH')
            }
            
            _UfjwiDSn = self._nEhmqhkg('epuTGgz74mksO2d8', '/_zJaCRjMB/_GNsihClY', _vNaWiklo=_vNaWiklo, _ARtGtjQR={'IfZKDrPgyuNYhPQw': _kVjSGhBD})
            logger._zgbWBQti(_cbvLfvdO"7TK8oqlfygevVMFa")
            _wCnIerFK _UfjwiDSn
            
        _HglOKkby Exception _VOAYmUJe _FVnNlLPT:
            logger._fpzJMFJz(_cbvLfvdO"oFiA8AaX3KlvIf5R")
            _JBQflebU Exception(_cbvLfvdO"oFiA8AaX3KlvIf5R")
    
    _lhoNVTJv _tiEFaDnF(self, _bNDDiMwP: str) -> _cKoJCJzC:
        "KKUsNhu81oxcn4uK""Mel9d01iSqFNpVLC""KKUsNhu81oxcn4uK"
        _wCnIerFK self._nEhmqhkg('FYA1V5txEFR5km0W', _cbvLfvdO'/_cZypazAJ/{_bNDDiMwP}')

    _lhoNVTJv _dhynJLdL(self, _euuQQIEn: str) -> _bsztUGVj:
        "KKUsNhu81oxcn4uK""Fe5yKiSDUzSF8M5r""KKUsNhu81oxcn4uK"
        _eNgwGHJL:
            logger._zgbWBQti(_cbvLfvdO"ZWqBLZu8k4G1njMd")
            _wKdnBesX = self._OQioAkJe._YCnnmAyt(_cbvLfvdO'{self._KQzLjuQS}/view', _QKUdCFOG={'DaJwMPH2HV8jWJLj': _euuQQIEn})
            _wKdnBesX._dRJFxodE()
            _wCnIerFK _wKdnBesX._bZgIXOXl
        _HglOKkby Exception _VOAYmUJe _FVnNlLPT:
            logger._fpzJMFJz(_cbvLfvdO"ONa2lqHXq2lH2x7b")
            _JBQflebU Exception(_cbvLfvdO"ONa2lqHXq2lH2x7b")

    _lhoNVTJv __del__(self):
        "KKUsNhu81oxcn4uK""TWrQqUC6s1aR7uFn""KKUsNhu81oxcn4uK"
        self._OQioAkJe._pyPyeifX()
        logger._cWhZbgHr("HMg30CJJk6lMR8tm")