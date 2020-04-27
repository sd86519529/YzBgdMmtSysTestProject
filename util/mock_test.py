from flask import Flask

app = Flask(__name__)


@app.route('/s', methods=['POST'])
def success():
    result = """
<FOX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>2020-04-13 17:10:16</DTSERVER>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECURITIES_MSGSRSV1>
        <XFERTRNRS>
            <TRNUID>test1</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <XFERRS>
                <SRVRID>900928870286</SRVRID>
                <XFERINFO>
                    <ACCTFROM>
                        <ACCTID>356980100101058173</ACCTID>
                        <NAME>猫抖供应链科技（杭州）有限公司</NAME>
                        <BANKDESC>兴业银行</BANKDESC>
                        <CITY>杭州</CITY>
                    </ACCTFROM>
                    <ACCTTO INTERBANK="N" LOCAL="Y">
                        <ACCTID>6214836123435683</ACCTID>
                        <NAME>靳伟</NAME>
                        <BANKDESC>招商银行</BANKDESC>
                        <BANKNUM>105100000017</BANKNUM>
                    </ACCTTO>
                    <CHEQUENUM>4524580</CHEQUENUM>
                    <CURSYM>RMB</CURSYM>
                    <TRNAMT>0.01</TRNAMT>
                    <PURPOSE>test1</PURPOSE>
                    <DTDUE>2020-04-09</DTDUE>
                    <MEMO>普通网银--提现</MEMO>
                </XFERINFO>
                <XFERPRCSTS>
                    <XFERPRCCODE>PAYOUT</XFERPRCCODE>
                    <DTXFERPRC>2020-04-09 10:32:18</DTXFERPRC>
                    <MESSAGE>交易成功</MESSAGE>
                </XFERPRCSTS>
                <CLIENTREF>test1</CLIENTREF>
            </XFERRS>
        </XFERTRNRS>
    </SECURITIES_MSGSRSV1>
</FOX>
""".encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/w', methods=['POST'])
def wait():
    result = """
    <FOX>
        <SIGNONMSGSRSV1>
            <SONRS>
                <STATUS>
                    <CODE>0</CODE>
                    <SEVERITY>INFO</SEVERITY>
                </STATUS>
                <DTSERVER>2020-04-13 17:10:16</DTSERVER>
            </SONRS>
        </SIGNONMSGSRSV1>
        <SECURITIES_MSGSRSV1>
            <XFERTRNRS>
                <TRNUID>test1</TRNUID>
                <STATUS>
                    <CODE>0</CODE>
                    <SEVERITY>INFO</SEVERITY>
                </STATUS>
                <XFERRS>
                    <SRVRID>900928870286</SRVRID>
                    <XFERINFO>
                        <ACCTFROM>
                            <ACCTID>356980100101058173</ACCTID>
                            <NAME>猫抖供应链科技（杭州）有限公司</NAME>
                            <BANKDESC>兴业银行</BANKDESC>
                            <CITY>杭州</CITY>
                        </ACCTFROM>
                        <ACCTTO INTERBANK="N" LOCAL="Y">
                            <ACCTID>6214836123435683</ACCTID>
                            <NAME>靳伟</NAME>
                            <BANKDESC>招商银行</BANKDESC>
                            <BANKNUM>105100000017</BANKNUM>
                        </ACCTTO>
                        <CHEQUENUM>4524580</CHEQUENUM>
                        <CURSYM>RMB</CURSYM>
                        <TRNAMT>0.01</TRNAMT>
                        <PMTMODE>SUPER</PMTMODE>
                        <PURPOSE>test1</PURPOSE>
                        <DTDUE>2020-04-09</DTDUE>
                        <MEMO>超级网银--提现</MEMO>
                    </XFERINFO>
                    <XFERPRCSTS>
                        <XFERPRCCODE>PENDING</XFERPRCCODE>
                        <DTXFERPRC>2020-04-09 10:32:18</DTXFERPRC>
                        <MESSAGE>未决</MESSAGE>
                    </XFERPRCSTS>
                    <CLIENTREF>test1</CLIENTREF>
                </XFERRS>
            </XFERTRNRS>
        </SECURITIES_MSGSRSV1>
    </FOX>
    """.encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/f', methods=['POST'])
def fail():
    result = """
       <FOX>
           <SIGNONMSGSRSV1>
               <SONRS>
                   <STATUS>
                       <CODE>0</CODE>
                       <SEVERITY>INFO</SEVERITY>
                   </STATUS>
                   <DTSERVER>2020-04-13 17:10:16</DTSERVER>
               </SONRS>
           </SIGNONMSGSRSV1>
           <SECURITIES_MSGSRSV1>
               <XFERTRNRS>
                   <TRNUID>test1</TRNUID>
                   <STATUS>
                       <CODE>0</CODE>
                       <SEVERITY>INFO</SEVERITY>
                   </STATUS>
                   <XFERRS>
                       <SRVRID>900928870286</SRVRID>
                       <XFERINFO>
                           <ACCTFROM>
                               <ACCTID>356980100101058173</ACCTID>
                               <NAME>猫抖供应链科技（杭州）有限公司</NAME>
                               <BANKDESC>兴业银行</BANKDESC>
                               <CITY>杭州</CITY>
                           </ACCTFROM>
                           <ACCTTO INTERBANK="N" LOCAL="Y">
                               <ACCTID>6214836123435683</ACCTID>
                               <NAME>靳伟</NAME>
                               <BANKDESC>招商银行</BANKDESC>
                               <BANKNUM>105100000017</BANKNUM>
                           </ACCTTO>
                           <CHEQUENUM>4524580</CHEQUENUM>
                           <CURSYM>RMB</CURSYM>
                           <TRNAMT>0.01</TRNAMT>
                           <PURPOSE>test1</PURPOSE>
                           <DTDUE>2020-04-09</DTDUE>
                           <MEMO>普通网银--提现</MEMO>
                       </XFERINFO>
                       <XFERPRCSTS>
                           <XFERPRCCODE>FAIL</XFERPRCCODE>
                           <DTXFERPRC>2020-04-09 10:32:18</DTXFERPRC>
                           <MESSAGE>交易失败</MESSAGE>
                       </XFERPRCSTS>
                       <CLIENTREF>test1</CLIENTREF>
                   </XFERRS>
               </XFERTRNRS>
           </SECURITIES_MSGSRSV1>
       </FOX>
       """.encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/ss', methods=['POST'])
def select_success():
    result = """<FOX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>2020-04-20 14:39:06</DTSERVER>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECURITIES_MSGSRSV1>
        <XFERINQTRNRS>
            <TRNUID>200420143204308496wd</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <XFERINQRS>
                <XFERLIST MORE="N">
                    <FROM>900930713607</FROM>
                    <TO>900930713607</TO>
                    <XFER>
                        <SRVRTID>900930713607</SRVRTID>
                        <XFERINFO>
                            <ACCTFROM>
                                <ACCTID>356930100100162454</ACCTID>
                                <NAME>杭州全游电竞信息科技有限公司</NAME>
                                <CITY>浙江省杭州市</CITY>
                            </ACCTFROM>
                            <ACCTTO INTERBANK="N" LOCAL="Y">
                                <ACCTID>6222081202013046600</ACCTID>
                                <NAME>潘晓琴</NAME>
                                <BANKDESC>中国工商银行</BANKDESC>
                                <BANKNUM>102100099996</BANKNUM>
                            </ACCTTO>
                            <CHEQUENUM>6010201</CHEQUENUM>
                            <CURSYM>RMB</CURSYM>
                            <TRNAMT>6194.00</TRNAMT>
                            <PMTMODE>SUPER</PMTMODE>
                            <PURPOSE>test1</PURPOSE>
                            <MEMO>超级网银--提现</MEMO>
                        </XFERINFO>
                        <XFERPRCSTS>
                            <XFERPRCCODE>PAYOUT</XFERPRCCODE>
                            <DTXFERPRC>2020-04-20 14:33:07</DTXFERPRC>
                            <MESSAGE>交易成功</MESSAGE>
                        </XFERPRCSTS>
                    </XFER>
                </XFERLIST>
            </XFERINQRS>
          </XFERINQTRNRS>
        </SECURITIES_MSGSRSV1>
       </FOX>""".encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/sn', methods=['POST'])
def select_no():
    result = """ <FOX>  
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>2020-04-21 12:04:02</DTSERVER>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECURITIES_MSGSRSV1>
        <XFERINQTRNRS>
            <TRNUID>test1</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <XFERINQRS>
                <XFERLIST MORE="N">
                    <FROM>-1</FROM>
                    <TO>-1</TO>
                </XFERLIST>
            </XFERINQRS>
        </XFERINQTRNRS>
    </SECURITIES_MSGSRSV1>
</FOX>""".encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/sw', methods=['POST'])
def select_wait():
    result = """
<FOX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>2020-04-20 14:38:07</DTSERVER>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECURITIES_MSGSRSV1>
        <XFERINQTRNRS>
            <TRNUID>test1</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <XFERINQRS>
                <XFERLIST MORE="N">
                    <FROM>900930713607</FROM>
                    <TO>900930713607</TO>
                    <XFER>
                        <SRVRTID>900930713607</SRVRTID>
                        <XFERINFO>
                            <ACCTFROM>
                                <ACCTID>356930100100162454</ACCTID>
                                <NAME>杭州全游电竞信息科技有限公司</NAME>
                                <CITY>浙江省杭州市</CITY>
                            </ACCTFROM>
                            <ACCTTO INTERBANK="N" LOCAL="Y">
                                <ACCTID>6222081202013046600</ACCTID>
                                <NAME>潘晓琴</NAME>
                                <BANKDESC>中国工商银行</BANKDESC>
                                <BANKNUM>102100099996</BANKNUM>
                            </ACCTTO>
                            <CHEQUENUM>6010201</CHEQUENUM>
                            <CURSYM>RMB</CURSYM>
                            <TRNAMT>6194.00</TRNAMT>
                            <PMTMODE>SUPER</PMTMODE>
                            <PURPOSE>test1</PURPOSE>
                            <MEMO>超级网银--提现</MEMO>
                        </XFERINFO>
                        <XFERPRCSTS>
                            <XFERPRCCODE>PENDING</XFERPRCCODE>
                            <DTXFERPRC>2020-04-20 14:33:07</DTXFERPRC>
                            <MESSAGE>指令处理中，请于10分钟后查询账户变动情况，如有疑问，请致电95561转4。</MESSAGE>
                        </XFERPRCSTS>
                    </XFER>
                </XFERLIST>
            </XFERINQRS>
        </XFERINQTRNRS>
    </SECURITIES_MSGSRSV1>
</FOX>""".encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/sf', methods=['POST'])
def select_fail():
    result = """
<FOX>
    <SIGNONMSGSRSV1>
        <SONRS>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <DTSERVER>2020-04-20 14:38:07</DTSERVER>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECURITIES_MSGSRSV1>
        <XFERINQTRNRS>
            <TRNUID>test1</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <XFERINQRS>
                <XFERLIST MORE="N">
                    <FROM>900930713607</FROM>
                    <TO>900930713607</TO>
                    <XFER>
                        <SRVRTID>900930713607</SRVRTID>
                        <XFERINFO>
                            <ACCTFROM>
                                <ACCTID>356930100100162454</ACCTID>
                                <NAME>杭州全游电竞信息科技有限公司</NAME>
                                <CITY>浙江省杭州市</CITY>
                            </ACCTFROM>
                            <ACCTTO INTERBANK="N" LOCAL="Y">
                                <ACCTID>6222081202013046600</ACCTID>
                                <NAME>潘晓琴</NAME>
                                <BANKDESC>中国工商银行</BANKDESC>
                                <BANKNUM>102100099996</BANKNUM>
                            </ACCTTO>
                            <CHEQUENUM>6010201</CHEQUENUM>
                            <CURSYM>RMB</CURSYM>
                            <TRNAMT>6194.00</TRNAMT>
                            <PMTMODE>SUPER</PMTMODE>
                            <PURPOSE>test1</PURPOSE>
                            <MEMO>超级网银--提现</MEMO>
                        </XFERINFO>
                        <XFERPRCSTS>
                            <XFERPRCCODE>FAIL</XFERPRCCODE>
                            <DTXFERPRC>2020-04-20 14:33:07</DTXFERPRC>
                            <MESSAGE>查询结果为提现失败</MESSAGE>
                        </XFERPRCSTS>
                    </XFER>
                </XFERLIST>
            </XFERINQRS>
        </XFERINQTRNRS>
    </SECURITIES_MSGSRSV1>
</FOX>""".encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


@app.route('/fl', methods=['POST'])
def select_long_remark():
    result = """        <FOX>
           <SIGNONMSGSRSV1>
               <SONRS>
                   <STATUS>
                       <CODE>0</CODE>
                       <SEVERITY>INFO</SEVERITY>
                   </STATUS>
                   <DTSERVER>2020-04-13 17:10:16</DTSERVER>
               </SONRS>
           </SIGNONMSGSRSV1>
           <SECURITIES_MSGSRSV1>
               <XFERTRNRS>
                   <TRNUID>test1</TRNUID>
                   <STATUS>
                       <CODE>0</CODE>
                       <SEVERITY>INFO</SEVERITY>
                   </STATUS>
                   <XFERRS>
                       <SRVRID>900928870286</SRVRID>
                       <XFERINFO>
                           <ACCTFROM>
                               <ACCTID>356980100101058173</ACCTID>
                               <NAME>猫抖供应链科技（杭州）有限公司</NAME>
                               <BANKDESC>兴业银行</BANKDESC>
                               <CITY>杭州</CITY>
                           </ACCTFROM>
                           <ACCTTO INTERBANK="N" LOCAL="Y">
                               <ACCTID>6214836123435683</ACCTID>
                               <NAME>靳伟</NAME>
                               <BANKDESC>招商银行</BANKDESC>
                               <BANKNUM>105100000017</BANKNUM>
                           </ACCTTO>
                           <CHEQUENUM>4524580</CHEQUENUM>
                           <CURSYM>RMB</CURSYM>
                           <TRNAMT>0.01</TRNAMT>
                           <PURPOSE>test1</PURPOSE>
                           <DTDUE>2020-04-09</DTDUE>
                           <MEMO>普通网银--提现</MEMO>
                       </XFERINFO>
                       <XFERPRCSTS>
                           <XFERPRCCODE>FAIL</XFERPRCCODE>
                           <DTXFERPRC>2020-04-09 10:32:18</DTXFERPRC>
                           <MESSAGE>交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败交易失败</MESSAGE>
                       </XFERPRCSTS>
                       <CLIENTREF>test1</CLIENTREF>
                   </XFERRS>
               </XFERTRNRS>
           </SECURITIES_MSGSRSV1>
       </FOX>
       """.encode('gbk')
    return result, 200, [("Content-Type", "text/html; charset=gbk")]


if __name__ == '__main__':
    pass
