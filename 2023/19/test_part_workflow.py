from copy import deepcopy

from pytest import mark

Part = dict[str, int]
Parts = list[Part]
Workflows = dict[str, str]


def part_workflow(input_string) -> int:
    workflows, parts = _parse_input(input_string)
    return sum(sum(part.values()) for part in parts if _run_workflow(part, workflows))


def part_workflow_combinations(input_string) -> int:
    workflows, _ = _parse_input(input_string)
    part_ranges = {"x": (1, 4001), "m": (1, 4001), "a": (1, 4001), "s": (1, 4001)}

    return _count_workflow_combinations(part_ranges, workflows, "in")


def _count_workflow_combinations(
    part_ranges: dict[str, tuple[int, int]], workflows: Workflows, workflow_name: str
) -> int:
    expression = workflows[workflow_name]
    return _evaluate_expression_combinations(part_ranges, workflows, expression)


def _evaluate_expression_combinations(
    part_ranges: dict[str, tuple[int, int]], workflows: Workflows, expression: str
) -> int:
    lt_loc = expression.find("<")
    gt_loc = expression.find(">")

    if lt_loc == -1 and gt_loc == -1:
        if expression == "A":
            output = 1
            for begin, end in part_ranges.values():
                output *= end - begin
            return output
        elif expression == "R":
            return 0
        else:
            return _count_workflow_combinations(part_ranges, workflows, expression)

    operator_loc = gt_loc if lt_loc == -1 else (lt_loc if gt_loc == -1 else min(lt_loc, gt_loc))
    colon_loc = expression.find(":")
    comma_loc = expression.find(",")
    operator = expression[operator_loc]
    lhs_operand = expression[:operator_loc]
    rhs_operand = int(expression[operator_loc + 1 : colon_loc])
    true_expression = expression[colon_loc + 1 : comma_loc]
    false_expression = expression[comma_loc + 1 :]
    true_ranges = deepcopy(part_ranges)
    false_ranges = deepcopy(part_ranges)

    if operator == "<":
        true_ranges[lhs_operand] = _update_range_lt(true_ranges[lhs_operand], rhs_operand)
        false_ranges[lhs_operand] = _update_range_ge(false_ranges[lhs_operand], rhs_operand)
    elif operator == ">":
        true_ranges[lhs_operand] = _update_range_gt(true_ranges[lhs_operand], rhs_operand)
        false_ranges[lhs_operand] = _update_range_le(false_ranges[lhs_operand], rhs_operand)
    else:
        raise RuntimeError("Oops")

    return _evaluate_expression_combinations(
        true_ranges, workflows, true_expression
    ) + _evaluate_expression_combinations(false_ranges, workflows, false_expression)


def _update_range_lt(range: tuple[int, int], value: int) -> tuple[int, int]:
    begin, end = range

    if value <= begin:
        return begin, begin
    elif value >= end:
        return begin, end
    else:
        return begin, min(end, value)


def _update_range_ge(range: tuple[int, int], value: int) -> tuple[int, int]:
    begin, end = range

    if value <= begin:
        return begin, end
    elif value >= end:
        return end, end
    else:
        return max(begin, value), end


def _update_range_gt(range: tuple[int, int], value: int) -> tuple[int, int]:
    begin, end = range

    if value < begin:
        return begin, end
    elif value >= end:
        return end, end
    else:
        return max(value + 1, begin), end


def _update_range_le(range: tuple[int, int], value: int) -> tuple[int, int]:
    begin, end = range

    if value < begin:
        return begin, begin
    elif value >= end:
        return begin, end
    else:
        return begin, min(value + 1, end)


def _run_workflow(part: Part, workflows: Workflows) -> bool:
    key = "in"

    while key not in {"A", "R"}:
        workflow = workflows[key]
        key = _evaluate_workflow(part, workflow)

    return key == "A"


def _evaluate_workflow(part: Part, workflow: str) -> str:
    lt_loc = workflow.find("<")
    gt_loc = workflow.find(">")

    if lt_loc == -1 and gt_loc == -1:
        return workflow

    operator_loc = gt_loc if lt_loc == -1 else (lt_loc if gt_loc == -1 else min(lt_loc, gt_loc))
    colon_loc = workflow.find(":")
    comma_loc = workflow.find(",")
    operator = workflow[operator_loc]
    lhs_operand = workflow[:operator_loc]
    rhs_operand = workflow[operator_loc + 1 : colon_loc]
    lhs_operand_value = _evaluate_operand(lhs_operand, part)
    rhs_operand_value = _evaluate_operand(rhs_operand, part)
    true_workflow = _evaluate_workflow(part, workflow[colon_loc + 1 : comma_loc])
    false_workflow = _evaluate_workflow(part, workflow[comma_loc + 1 :])

    if operator == "<":
        return true_workflow if lhs_operand_value < rhs_operand_value else false_workflow
    elif operator == ">":
        return true_workflow if lhs_operand_value > rhs_operand_value else false_workflow

    raise RuntimeError("Whoops")


def _evaluate_operand(s: str, part: Part) -> int:
    if s.isdigit():
        return int(s)

    return part[s]


def _parse_input(input_string: str) -> tuple[Workflows, Parts]:
    lines = input_string.splitlines()
    index = 0
    workflows: Workflows = Workflows()

    while lines[index]:
        _parse_workflow(lines[index], workflows)
        index += 1

    index += 1

    parts = []
    while index < len(lines):
        parts.append(_parse_part(lines[index]))
        index += 1

    return workflows, parts


def _parse_part(s: str) -> Part:
    tokens = s[1:-1].split(",")
    output = Part()

    for token in tokens:
        equal_loc = token.find("=")
        output[token[:equal_loc]] = int(token[equal_loc + 1 :])
    return output


def _parse_workflow(line: str, workflows: Workflows) -> None:
    open_brace = line.find("{")
    name = line[:open_brace]
    workflows[name] = line[open_brace + 1 : -1]


EXAMPLE_INPUT = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""
PUZZLE_INPUT = """pnv{a<2630:R,A}
qpv{x<1782:fng,x<2737:R,A}
btl{s>2396:A,R}
cq{m<3505:A,m<3705:A,a>1266:R,R}
zf{a<363:xql,bgx}
ncc{m<2660:R,x>1277:A,a<1366:R,R}
xql{x>939:R,x>386:R,R}
sqc{s<2972:A,A}
tdq{s>2439:zq,s<2392:qz,s<2422:gss,gzh}
jjl{s<848:R,A}
sb{m<1868:qx,x>2338:kpq,s>1982:jf,hd}
pc{x>1519:A,s<1677:R,s<1789:R,fn}
xm{m<1795:mm,a>1313:xzg,nt}
qrl{x<2554:tjx,s>1612:cj,sq}
df{a<317:A,s<130:R,s<147:R,R}
spp{x<2189:A,A}
qqz{a>2735:A,m>3070:gv,R}
xf{a<1152:A,a>1282:R,s<1142:A,R}
ktg{m>1334:A,x<3202:A,s<939:R,vkx}
hgv{m<648:vm,a<1062:R,x>1854:qs,A}
gz{s>3829:R,a<800:A,R}
tcp{x>3555:A,R}
jgh{m>2442:xrt,x>1879:ct,dn}
qk{x>2955:ln,m<2753:jl,m>3239:gj,kt}
dzz{s<645:A,mfh}
flz{x<3157:A,x<3324:R,A}
qv{m<1163:R,m>1940:A,R}
qfl{a>574:vl,s>2971:qhx,s<2767:tn,tlj}
mlc{s>1250:A,s>1120:R,m>2730:R,A}
hkh{x>2796:A,R}
jn{m<2451:gp,R}
rgh{a<322:R,A}
jr{m>2821:xsl,a>2413:R,R}
zl{x>773:A,a<1392:xf,R}
ndg{a<3811:A,s<2933:A,a>3880:A,R}
hqz{s<1513:A,R}
tlj{m>1531:jc,hq}
rpk{a<159:mjb,lzh}
brs{x>2340:R,x<1218:R,A}
bh{s>45:rsg,m<630:brs,R}
qhx{a>368:fz,s>3161:tp,dq}
xvk{m<1424:dg,m>2965:rk,mqb}
nmm{a<330:R,a<463:A,a<495:R,R}
nxf{x>3610:A,x>3400:A,x<3264:A,R}
ghp{x>1386:jr,lg}
slx{s>3458:A,s<3251:A,R}
crk{s<759:A,m<2715:R,A}
mvm{s>285:fb,s<96:mt,x<1994:sxl,tpx}
gd{a>1402:ft,s<3094:mtv,a<1203:rpx,xm}
bt{a>1843:sp,m<2632:dj,R}
xp{x>502:R,s>2643:A,A}
nf{s<2944:A,a<1266:R,m>2113:R,A}
fbj{m<1833:A,s>3143:A,A}
lp{m>2247:A,x<2896:A,s>1662:A,A}
xl{s>1633:R,s<1562:R,s<1604:A,R}
zjd{x>2566:R,s>3638:R,x<2076:R,R}
qft{a>993:A,m<3431:R,A}
tn{x>1053:fr,s>2699:A,s>2661:nb,xp}
ggd{a>690:R,s<374:R,s>490:A,A}
bg{s<1514:hh,x<3785:R,m<1098:bsv,R}
mk{s>2443:R,a>142:ghz,s<2371:A,hm}
qjf{s<209:zt,s>250:ssm,m<402:R,vbr}
lf{s<3464:A,xb}
mfh{s>975:A,R}
jbf{a<1178:R,m<1644:A,R}
hqx{a<75:A,R}
mt{a>517:rlg,a<337:tgr,bh}
kp{x>243:R,x>162:A,R}
jjd{a>227:R,A}
vzl{m>3320:R,a>747:A,ggd}
bqf{x<392:fj,jld}
lq{x>2656:R,A}
gnx{a<1409:R,x>2669:R,R}
sbk{s>176:kzc,s<134:R,vn}
ftd{m>3310:A,R}
mtv{s>2818:srk,tf}
hvg{a<184:A,a>361:R,m>353:R,A}
dnh{s<2051:hvj,xz}
rk{a>3410:lvm,s<3154:rpq,m<3319:xkb,zb}
bbd{m<1648:R,R}
vn{x<1218:R,R}
rxm{m<3037:A,a<3652:A,a<3783:A,R}
lhr{x<977:R,s<2606:R,a>1061:R,R}
bz{x>356:R,A}
gvs{s>227:R,A}
rxh{s<1996:R,s>2027:R,s>2007:R,A}
vvc{x<2607:R,s<513:xln,s<846:lk,A}
qc{s>2515:tdr,s<2409:R,mgh}
vtj{s<1147:R,s<1283:A,x>2934:A,A}
zt{s>139:R,x>1411:R,s>118:R,R}
dqz{s<1321:A,a<2606:R,a<2895:R,A}
rp{m>2386:R,R}
lt{s>2777:R,s>2705:R,A}
dl{s>312:A,a>137:R,s>259:A,A}
qz{a>663:zm,a>409:kd,R}
nzh{x<3109:xq,a<2613:R,x<3252:ss,R}
nlz{x>3224:A,A}
fkx{x<2574:R,s>960:fps,A}
qh{m>1152:R,a>680:R,s>1682:tg,pr}
hrm{a>546:xhg,m>879:ktg,s>1067:lhg,sl}
hd{a<938:mc,x<1690:vq,R}
szr{m>1603:kcn,s>531:cbn,m<1033:mvm,ch}
jc{s<2856:R,x<1048:A,A}
dj{a>950:A,s<1785:R,m<2205:A,A}
cj{x>3311:jjj,s>1751:pz,m<1872:cvk,qk}
kt{x>2694:tmp,m>2949:R,a>1543:R,A}
xjd{s<3105:A,a>2050:R,m>1463:A,A}
cgg{m<625:R,bgl}
ls{a>475:A,A}
jpr{x<736:sx,s<3350:A,jsk}
dvf{a>1537:qld,s>964:jzj,s<422:hhr,vgs}
tth{m>461:A,m>282:A,m>170:R,R}
hj{s>3109:R,a<124:R,s<2949:A,A}
tng{a>751:A,s>1079:A,x<1326:A,R}
ngx{s<384:lc,dp}
nc{s<1916:A,a>1035:R,s<1922:R,R}
mf{s<205:R,a>166:A,a>94:A,A}
vrr{a>2625:A,x<2277:R,R}
vxx{x>1741:bjm,m>1905:R,m>1559:A,A}
jt{x>3716:R,x>3650:R,R}
lhs{x>2681:A,a<2540:R,R}
lcn{m>755:A,s>1214:R,m<469:R,A}
lln{s<445:R,m<268:R,s<461:A,A}
hm{x>1734:R,s<2410:A,A}
mp{m<711:lkj,A}
nj{m>1713:A,m<1125:A,A}
cb{m<3049:jgk,x>2784:R,R}
krl{a>1348:A,s<628:R,R}
sh{a>1276:R,R}
fn{a>3050:A,a<2792:A,A}
bb{s<163:vsx,s<243:dld,A}
bc{a>2046:jgh,a>914:lng,szr}
lk{x<3283:A,a<1900:R,A}
sl{x<3264:hkh,s>715:cqr,x<3740:znr,nmm}
mq{m<526:bqr,dzf}
vdn{a>790:A,m>2018:R,a>456:mx,A}
cjz{s<832:R,x<1390:R,A}
chn{m<1834:bg,lkh}
bcc{x>917:A,R}
jrf{s>473:xtn,s>424:A,s<393:R,hps}
xpn{x<3290:spz,x>3623:stf,m<764:dqz,A}
fxj{x>1787:xvk,zbk}
nt{m>2968:cq,m>2511:R,sh}
fjh{a>330:A,m>1524:A,m>1492:R,A}
xq{s<1556:R,m>1439:A,A}
km{s>1752:R,R}
qg{a<3374:A,a<3747:A,A}
ps{a>666:R,x<3515:A,m<1018:R,A}
ctm{m<3241:A,R}
gf{s>2707:A,R}
vrp{m<952:pd,A}
in{s>2630:ld,s>1462:nkf,bc}
kzc{m<484:R,m>687:A,A}
rfl{s>2193:kr,x>1357:fm,m<1863:cg,bhz}
rll{s>336:R,s<201:bpt,x<2238:kg,zbx}
bm{x>1200:btl,a>1179:jj,mjv}
tp{m>1670:A,s>3243:R,m>1085:R,R}
mjb{a>58:R,m>2431:A,m<2129:R,R}
ch{m>1301:vmv,hn}
nrn{s>2068:rfl,x<1344:vmk,sb}
thc{s>1780:R,s>1682:phd,pzp}
cnd{x<3374:A,R}
csm{a>446:xrr,a<189:nh,x>450:hdp,pb}
fpl{a>1650:kcz,s<2305:nrn,x>2628:dmx,lj}
dvp{x>2084:lr,s<3287:qfl,m>2644:kf,gvt}
qfh{m<3214:R,x<2287:A,A}
vk{a<3396:hqz,s<1560:qj,s<1592:R,flz}
mx{s>1971:A,x>477:R,s<1954:R,R}
fj{s<303:kp,s<476:R,m>1310:R,R}
qj{s<1527:A,A}
lkj{m<432:A,m>577:R,m<510:R,A}
srk{x<1497:A,a>1169:nf,a>1049:pf,A}
lzh{s>537:A,x>965:A,A}
zq{s<2562:A,x<3107:xv,s>2592:A,R}
lg{m<2702:R,x>582:mv,A}
zcm{a>3555:vdf,s<3451:A,cpm}
dxb{x<3257:rb,x>3685:R,m<2129:ps,bq}
sk{s>1525:R,A}
sn{x<3897:R,s>1539:A,s>1507:A,A}
dmx{m>2059:ccd,tdq}
xvn{m<351:R,x>2393:R,R}
vvd{x>2974:zp,R}
lcc{m>3177:A,s>2384:A,A}
cc{x>2435:A,s<191:ql,R}
pm{a<1388:R,s>2500:R,m>1439:A,ts}
hb{x<2496:R,m<2726:R,x<3383:A,nch}
zgl{s<635:lq,x>3156:pfq,cdz}
mr{x>1745:vrp,zl}
vpp{s<242:tth,s>257:qd,A}
lnk{m<2592:qtm,R}
jbr{x>788:R,x<474:R,s>3470:A,R}
qdv{x>2652:A,m>1433:R,R}
spg{s<2353:R,x>1228:A,x<750:R,A}
lvb{a<473:R,x<3266:R,m<939:A,A}
jrj{m>3129:A,a>662:R,R}
fm{s>2117:R,s<2092:vhn,x<2631:A,A}
ndm{s>365:jrf,vfq}
pv{x>1589:zfz,A}
ckk{s>236:bk,m<3187:A,x<3279:dx,mxp}
pg{a<339:mk,m<2499:qc,ftd}
npc{a>466:A,R}
db{x<1464:lnk,crf}
qx{x<3100:kx,m<1031:R,dgq}
zfq{a>524:A,A}
fjs{x>3200:R,a<146:A,x>2874:lcc,jjd}
zp{a>1395:A,A}
lvm{s<3328:trh,m>3505:R,ghj}
kng{s<2493:bm,m>3452:xgh,fgr}
qq{s>2432:R,A}
mb{m>1445:bcc,a<2795:R,A}
hr{m>1150:R,m>443:cbh,a<640:A,A}
rqn{x>2195:A,a<1290:A,x>1119:R,R}
thv{x>2809:A,x>2419:A,m<571:R,R}
ssr{s<1168:lgk,m<559:dh,a>3139:lbs,xpn}
kg{s>272:R,m<1454:A,R}
dn{x>1084:lz,s>593:bx,bqf}
cf{m<639:A,s<3221:pp,x>3541:ds,fvc}
pp{a<2936:R,x>3345:A,R}
td{a<1277:hgv,x<2074:bht,s>306:gcn,vvd}
cg{x>672:R,R}
fxk{x<3348:A,A}
xtn{m>2134:A,x<1811:A,m>1892:A,A}
tg{m>673:A,m<314:A,R}
kcf{x>608:R,x<205:ntp,R}
tgz{a>1754:A,R}
qt{x>2921:xpd,a>1995:xdf,x<2722:sk,ltt}
dld{x<494:A,s<199:R,R}
mjv{m<3208:A,m<3702:R,s>2384:A,A}
hps{m>2250:R,s<405:R,a<599:A,A}
kjh{a>3337:R,m<464:A,s>1385:A,R}
pz{a>2318:ht,vvp}
rc{s<262:R,x>811:R,A}
ds{x<3721:R,s>3699:R,s>3476:R,A}
ntp{x<77:R,R}
jld{m>951:R,a>3233:rc,a<2643:qjp,A}
mpj{a<666:fkx,lvv}
zfz{x<1630:R,x<1657:R,A}
ck{s<962:zsj,a>3138:hbx,xfc}
bk{m>3452:R,R}
cnj{s>1763:A,a>2468:cnd,s>1690:R,A}
zcz{m<2232:R,s<1682:A,A}
zbx{m>1431:A,x<2914:A,s<258:A,A}
crf{x>1600:R,s<3236:sqc,jqh}
lr{a>481:dxb,m<2629:lpq,x<3259:dd,qqc}
vkx{s<1200:R,a<261:A,R}
qtm{s<3529:R,a<3184:A,m>2279:A,A}
nmv{m>768:R,A}
brt{m>354:R,s<493:R,s<646:R,R}
pzd{a<855:zcz,m<1853:ccv,m<3101:zk,hmd}
sgp{s>3593:R,x<813:A,R}
kvg{m>2928:R,R}
ckp{m>3627:A,R}
dgq{x>3537:R,R}
rlg{x>1387:cqt,m>554:R,a>654:A,jmx}
xgh{s>2546:R,a>1311:A,tc}
sj{a>643:R,a>585:A,x>1738:R,R}
mqb{a<3391:lnm,s>3381:qr,njj}
jgm{s>2750:R,R}
lqp{s>1248:A,R}
gc{m>3241:rqn,m<3136:R,m<3179:R,qkb}
lgp{m>866:A,m>755:A,m>671:ls,vhc}
kvl{x<1422:A,a>3024:A,R}
cdz{a>137:R,R}
rld{a>2992:R,x>2926:A,R}
jj{m>3310:A,m<2977:A,A}
njj{a<3680:cth,ndg}
pfq{m>3025:A,a>193:R,a<87:R,A}
rpq{s<2866:lt,m>3459:cp,pnv}
qkb{x<2298:R,a<1313:R,m<3212:R,A}
jsk{a>2739:A,A}
szz{s>2350:A,A}
xj{s<3270:R,m<2735:A,m>3433:A,R}
jb{s>716:R,x<1196:R,R}
mvv{a>908:gd,dvp}
rfv{s>1017:hrf,x>1232:mp,csm}
hrf{a>604:R,x>1186:R,x<617:kz,glk}
gxb{s<2420:vx,pm}
lhh{m<657:R,x<3667:A,A}
pb{a<287:A,R}
bp{a>1592:ppj,R}
xqb{x>1364:ngd,x<772:mxk,R}
ln{s<1690:lmt,A}
kk{m>3273:A,a<867:R,A}
nx{m>2232:jpg,A}
gx{a>1776:R,R}
xv{a>580:R,A}
dk{m<1515:gr,kvl}
hgl{a>2798:tnf,m>3465:mmm,dzz}
vm{s<397:R,x>2464:A,A}
nkf{s>1890:fpl,qrl}
bsv{a>1977:A,A}
cbn{x>2136:hrm,rfv}
gzh{a<955:lvb,a>1251:qq,x<3426:R,A}
cpm{x<850:A,A}
phd{a<1873:R,R}
ccc{x<1738:A,a>2960:brt,A}
nz{m>1580:A,m>535:rs,a<3608:xvn,bv}
hmd{a<1503:R,x>1671:xl,A}
qs{s>337:R,A}
tjx{a<2514:pzd,x<1218:nxd,x>1675:zgp,qdl}
dzf{m<883:R,s<268:dmr,tgz}
dh{s<1310:A,m>372:kjh,glr}
gj{x<2764:R,ckp}
fr{s<2699:A,m<1878:A,A}
vmk{s>1989:fbc,s<1935:ll,vdn}
vmh{s<2090:A,A}
ss{a>2750:A,A}
bqr{a<1774:A,m<177:R,R}
jk{a<1028:R,s>3587:R,a>1091:R,A}
xln{a>1888:R,s>294:R,R}
zmz{x>1081:R,A}
mpb{s>2362:R,a<467:R,R}
zd{s>3154:R,s>3055:A,A}
nsj{x<1701:A,a>1055:A,A}
xsl{s>511:A,s<282:R,a<2317:R,R}
tgr{m>684:A,s<48:A,pmn}
ghj{s<3589:R,x>2695:R,m>3158:R,A}
kr{s<2240:R,m<2537:qv,m<3458:R,cm}
jx{s>3380:A,a>1102:A,s>3274:A,R}
ngd{m<2862:R,A}
vhn{a<1080:A,s<2081:A,s<2087:A,R}
gm{a<1387:jrj,a<3054:jsb,x>3816:R,jt}
qr{s<3607:R,s>3740:R,s<3694:zjd,A}
sq{x>3517:chn,lrm}
jl{x>2790:lp,m>2443:gnx,A}
cqb{m<3291:R,m<3385:R,x<942:R,A}
ql{x<1292:R,m<1982:R,x>1755:R,R}
fnz{s>792:mr,a<1529:td,mq}
xb{s<3532:R,s<3567:A,A}
bdp{a<3499:A,m<1904:A,m>2112:R,R}
gv{x>604:R,s>3769:R,a>2546:A,R}
fvc{a>2712:R,A}
hh{s>1493:A,a>1779:A,R}
ftr{x>2560:A,x<1662:R,x>2139:R,A}
lpq{a<194:hj,m<1056:qn,m<1753:R,A}
rb{x<2494:R,A}
txh{a<796:A,a>847:A,m>2443:R,A}
tk{m<3086:sbf,m>3574:R,kk}
pvh{a<1254:A,A}
ppj{m>2232:A,a<1757:A,x>812:R,R}
vx{m>1190:szz,spg}
kz{a>230:A,s>1293:A,R}
stf{s<1343:R,R}
xrt{m>3080:hgl,a>2847:vj,ghp}
bf{a<1198:A,A}
zb{x>2686:A,a<2867:vrr,m>3738:ndd,spp}
dc{x<2379:R,a>457:A,R}
zn{a<3249:R,m<3107:R,m>3180:R,A}
kv{s>3704:R,R}
tpx{s<182:mfm,vpp}
mm{x>1494:slx,sz}
lrm{a<1813:rdj,a>2956:vk,a<2277:qt,nzh}
fzr{x>418:R,s<3682:A,A}
hkb{x>224:qvs,a<3369:R,rxm}
pt{s>3351:R,R}
xhg{s<957:R,R}
mtm{m>1488:A,m>1419:R,A}
nh{m<986:A,R}
msz{x>2122:A,x>1082:A,m<992:A,R}
hk{x<3155:npc,mpb}
xdf{m<1884:R,R}
vz{s>3672:R,sj}
fps{a>512:R,s>1158:R,m<3095:R,A}
bqx{m>2983:R,m>2337:A,m>2020:fzr,R}
lqz{a>163:R,m>1175:hqx,a<77:zrb,A}
dts{x<2728:A,x<3473:A,R}
hvf{s<139:R,m<482:R,m<734:A,A}
pl{a>1712:gx,zdz}
rpx{m<1653:hl,m<2556:lpc,qp}
ht{s>1809:A,s>1779:fd,R}
hhk{a<2872:qpv,nz}
dx{m<3625:R,x>2757:A,m<3826:A,A}
shz{x>694:jb,a>1411:A,x>244:krl,A}
xz{a>2779:A,R}
fz{a>475:R,R}
sdp{a>1363:A,R}
knd{a<2848:R,s>3383:jbr,xj}
gmm{s<1779:A,x>1234:A,m>345:A,R}
nxd{m<2019:kcf,x<633:hkb,fc}
fbc{x<750:A,a>1007:R,x<1082:A,R}
gpr{s>154:A,R}
xpj{x>3136:R,x>2671:mtm,zfq}
lpc{x>1928:R,m<2171:jk,A}
hq{a<277:A,R}
fhg{x<1615:R,A}
vsx{x>569:A,R}
qp{a>1091:A,s<3428:xnh,x>2584:R,qft}
mmm{m<3811:R,cjz}
glr{x<3098:R,R}
bht{x<1209:A,a>1367:kxq,R}
prj{x<2013:mb,m>2087:vmh,m<1061:dnh,gb}
dd{a>306:A,A}
kpq{m<2914:rxh,s>1966:nlz,R}
vmv{a<449:cjm,a>634:rll,x<1892:nzz,xpj}
xzg{x<2275:ncc,A}
zdz{a>1510:R,A}
pjn{m>1910:qfh,A}
qd{a>320:A,A}
cp{a<2845:A,x<2968:R,R}
jm{s<3150:rj,a>3314:bqx,s>3614:qqz,knd}
jz{x<3226:A,lhh}
mxp{s>81:R,x>3750:A,m>3590:A,R}
gb{s>2072:A,s<1981:A,x<3200:lhs,R}
vfq{m>2153:R,a<643:dc,a<792:gpr,cl}
trh{m>3392:A,x>2988:R,R}
tdr{s<2570:A,R}
dmr{m<1256:R,A}
qkg{a>713:R,x>867:A,a<643:A,R}
xc{x>2770:R,a<2515:A,s<1259:R,A}
tmp{a>1809:R,a>942:R,A}
bgl{s>1660:A,m>1423:R,s<1630:R,A}
kc{x>2390:bf,x<1059:pvh,x<1895:A,R}
tc{s>2511:R,a<1074:R,R}
lkh{x<3836:R,x>3940:jv,sn}
bjm{s>342:R,a>3165:A,m>1808:R,R}
hhr{m<2980:cc,m>3577:kc,s<184:jsj,gc}
zgp{x<2034:nx,pjn}
sx{x>306:A,a<2711:A,m<850:A,R}
lqg{x>2351:rld,a<3099:A,A}
bv{s<2491:A,m<249:R,A}
ft{a>1886:xjd,s<3269:pl,x<1697:bp,np}
xkb{s>3481:R,s<3263:A,a>2939:zn,pt}
mgh{x<1518:A,x>2108:R,A}
jjj{m<1876:thc,x>3613:gm,x>3437:bt,cnj}
fd{a>3430:R,x<2979:A,A}
tf{s<2703:nj,a>1224:ftr,a<1106:R,jgm}
zm{m<849:R,s>2341:A,m<1280:A,R}
nch{s<1100:R,R}
vq{s<1933:A,x<1561:R,R}
cbh{a>623:A,x<523:A,A}
rdj{s>1550:jbf,s<1497:R,a>932:A,R}
gcn{a<1424:R,R}
jzj{s<1171:hb,slf}
mxk{s<1062:R,s>1266:A,R}
vhf{a<2740:jjl,R}
lj{a<934:pg,m>2585:kng,gxb}
pq{m>2513:R,A}
vl{m<2010:R,s<2957:qkg,x<1175:zd,R}
ld{a<2237:mvv,fxj}
bgx{s<3944:R,A}
cqr{x<3595:R,x>3795:A,x<3671:A,A}
bx{x>636:gfl,s<983:vhf,ff}
rs{x>1579:R,a>3475:A,s>2511:R,A}
sz{s>3646:R,R}
pmn{x>1539:A,A}
gvt{a<546:sgp,a>695:hdl,x<1233:hr,vz}
jsj{s<105:A,a<1240:nsj,x<1500:A,R}
mdk{s<130:R,a<563:R,A}
jmx{a>603:R,s<41:A,A}
vcp{m>730:qg,R}
cl{a<836:A,R}
qjp{s<283:R,x>803:R,a<2283:A,A}
cqt{m>417:A,m>266:R,x>2900:R,A}
kf{s<3586:lf,s<3846:kv,zf}
qdl{m>1930:pc,x<1509:vcp,pv}
mc{m<2937:R,s<1930:A,a>390:A,R}
sxl{a<340:xxv,a<621:sbk,x<891:bb,qjf}
jv{s>1529:A,a<2108:A,s<1494:A,A}
zsj{x>2818:A,a>2925:bdp,A}
lz{x<1604:dk,s>880:vnf,m>954:vxx,ccc}
zk{a<1521:R,s<1702:R,R}
xnh{x>2153:R,s<3238:R,x<914:R,R}
kcz{s>2296:hhk,prj}
gr{x<1259:A,s<776:R,a<2702:A,A}
ssm{a<734:A,R}
vgs{x>1485:cb,a>1244:shz,jn}
jf{x>1956:R,A}
bhz{s<2114:gcv,gt}
rj{s>2827:R,m>3227:gf,m>2511:R,A}
hn{a>386:gvs,lqz}
fc{x>865:zmz,xk}
lnm{a>2827:rv,s>3525:px,m<2330:fbj,A}
vd{a<1181:R,s>2382:A,R}
gmx{a>638:vzl,x>2091:ckk,cqf}
rsg{a<432:A,m>392:R,R}
slf{a<1236:qtb,sdp}
vbr{m<712:R,a>785:A,x>1393:R,R}
gp{m>2108:R,A}
kx{s>1974:A,m<941:R,x>2212:A,R}
tpr{s<402:R,R}
vfb{x>1558:zgl,rpk}
qtb{a<1126:A,x<1551:A,A}
vfv{m<2751:A,a>792:R,x>3384:R,A}
rv{s>3267:A,a>3050:R,A}
jqh{m<2802:R,x>1517:A,m>3555:R,R}
zrb{a<29:A,A}
qvs{a>3460:A,R}
xfc{m>1552:xc,m<1118:vtj,m<1343:dts,qdv}
ghz{s<2396:R,R}
mv{s<859:A,R}
nb{a>311:A,m<2508:A,R}
dp{x>2605:R,x>2179:A,A}
dg{a>3288:jz,x<2829:nmv,cf}
lmt{a>1859:A,x<3172:A,m<3051:R,A}
hbx{s<1132:A,s>1343:R,mjk}
fb{x>1481:khb,m<566:vs,lgp}
ltt{m<1817:A,x>2809:R,A}
lng{m<1451:fnz,dvf}
sp{a<3159:A,m<3061:R,x>3524:R,A}
cn{s<3359:R,A}
jgk{s>647:R,x>2716:A,A}
vnf{x>1731:lqp,m>1250:lqs,R}
kd{x>3161:A,x>2922:A,R}
jsb{a<2292:R,s>1782:R,R}
ct{m>893:ck,s>737:ssr,ngx}
xxv{x<960:A,x<1435:R,mf}
ccd{s>2444:tk,a>600:nft,a<355:fjs,hk}
hdp{x<886:R,a<315:R,s>817:A,A}
mcl{x>1479:crk,s>917:mlc,A}
fng{m>1498:A,s>2431:R,A}
qld{a>1781:vvc,s<844:fhg,rp}
vvp{a<1484:A,A}
sg{a>2999:zcm,jpr}
khb{a>410:R,tpr}
kxq{s>301:R,A}
lgk{a>3037:A,a>2390:thv,R}
gss{x<3357:A,A}
vs{s<404:A,a<548:hvg,s>482:R,lln}
ccv{s<1665:A,a>1628:km,m>875:tr,gmm}
vhc{x<871:R,s>388:R,A}
qn{m>579:R,x>3125:A,x>2759:R,A}
dq{m>1918:A,a<172:R,x>1349:R,A}
bq{a<759:R,a>819:A,s<3288:R,A}
mjk{a<3562:R,a<3716:A,A}
cjm{m<1454:R,s<187:A,a<256:dl,fjh}
xk{a<3463:R,x>754:R,a>3650:A,R}
vj{a>3232:mcl,s<598:lqg,xqb}
zbk{m<1827:sg,x>1184:db,jm}
ndd{m<3911:A,a>3080:A,a<2996:R,R}
tnf{s<961:xs,x>1532:A,m>3522:A,cqb}
znr{s<597:R,s<666:R,R}
np{x>2742:fxk,A}
xpd{x>3136:A,a>2086:A,x>2997:R,R}
hdl{s>3542:gz,x>944:hs,bbd}
nft{x<3396:R,m>3126:vd,pq}
pr{a>419:A,a>243:R,A}
fgr{a>1184:R,s<2567:A,s<2590:R,lhr}
vdf{s<3350:A,A}
xs{a<3237:R,s>338:R,m<3679:R,R}
mfm{x<3090:df,nxf}
nzz{s<331:mdk,s>409:R,A}
tr{s<1743:R,x>936:A,x>362:A,R}
sbf{s>2521:R,R}
pzp{a<1728:R,R}
glk{a>351:A,x>867:A,A}
jpg{m<3010:R,m<3478:R,s>1647:R,A}
spz{a>2607:A,s>1333:A,a<2305:A,R}
gt{s>2151:A,m>2995:R,A}
ff{a>3010:A,m>1179:bz,lcn}
cvk{a<1930:qh,cgg}
gfl{s<1019:A,x>840:R,A}
xrr{x<631:R,R}
lvv{s<881:txh,x<2522:tng,s<1109:vfv,kvg}
ts{a<1524:A,A}
hl{s<3584:jx,s<3771:A,a<1065:msz,R}
cqf{s>350:ctm,s<182:A,A}
cm{x>2056:A,x>1026:R,a<946:A,R}
ll{x>459:nc,a>945:R,R}
hs{a>784:R,m>1014:R,R}
lqs{m<1973:A,m<2168:R,m>2340:A,A}
lbs{s>1323:A,m>718:R,A}
px{m<2194:A,a>2538:R,a<2365:A,R}
pd{m<476:A,s<1186:R,x<2630:R,A}
kcn{a<355:vfb,s>570:mpj,m<2618:ndm,gmx}
lc{x>3258:tcp,x<2482:hvf,m<507:R,A}
lhg{m<567:A,rgh}
gcv{x>597:R,m>3047:R,m>2314:R,A}
cth{m>2292:R,A}
pf{m<1678:A,x<2338:A,A}
hvj{a>2790:R,x<2727:R,a<2232:A,R}
bpt{x<2602:R,R}
qqc{m<3472:cn,A}

{x=1691,m=2832,a=1861,s=2722}
{x=1323,m=500,a=189,s=322}
{x=1650,m=26,a=322,s=1579}
{x=1176,m=1444,a=470,s=100}
{x=1714,m=1825,a=3429,s=1961}
{x=1107,m=133,a=36,s=1487}
{x=46,m=997,a=1512,s=1304}
{x=11,m=194,a=215,s=1000}
{x=921,m=2809,a=544,s=1593}
{x=202,m=203,a=40,s=104}
{x=1232,m=2102,a=666,s=679}
{x=70,m=350,a=94,s=264}
{x=2037,m=1015,a=3001,s=1221}
{x=96,m=540,a=686,s=138}
{x=1186,m=2459,a=470,s=3194}
{x=1144,m=59,a=3193,s=520}
{x=254,m=2234,a=1119,s=5}
{x=2979,m=154,a=1684,s=2303}
{x=573,m=138,a=1567,s=2914}
{x=361,m=143,a=1163,s=2996}
{x=1412,m=1218,a=1248,s=1255}
{x=583,m=1,a=133,s=1203}
{x=205,m=964,a=95,s=460}
{x=763,m=60,a=126,s=1095}
{x=1328,m=2904,a=67,s=76}
{x=1155,m=27,a=254,s=977}
{x=131,m=2544,a=368,s=298}
{x=1002,m=507,a=1287,s=224}
{x=349,m=1553,a=502,s=2106}
{x=1550,m=1556,a=1485,s=171}
{x=1390,m=330,a=235,s=516}
{x=1322,m=1984,a=98,s=182}
{x=472,m=449,a=28,s=3333}
{x=296,m=447,a=588,s=1863}
{x=325,m=2557,a=346,s=843}
{x=529,m=44,a=211,s=736}
{x=2226,m=444,a=179,s=194}
{x=155,m=584,a=5,s=461}
{x=595,m=1586,a=650,s=527}
{x=24,m=34,a=1084,s=1187}
{x=1157,m=1256,a=14,s=232}
{x=2423,m=60,a=1070,s=3013}
{x=2336,m=393,a=26,s=112}
{x=3260,m=227,a=1312,s=163}
{x=2094,m=75,a=43,s=1741}
{x=270,m=2166,a=964,s=45}
{x=1742,m=4,a=574,s=752}
{x=1839,m=189,a=503,s=796}
{x=1047,m=163,a=983,s=660}
{x=389,m=2269,a=1453,s=55}
{x=632,m=245,a=114,s=1752}
{x=30,m=195,a=483,s=90}
{x=2307,m=13,a=637,s=2864}
{x=1790,m=122,a=1979,s=482}
{x=16,m=296,a=2426,s=2718}
{x=88,m=2106,a=1744,s=18}
{x=614,m=258,a=1792,s=675}
{x=464,m=128,a=1600,s=540}
{x=1466,m=10,a=1698,s=337}
{x=1368,m=84,a=1120,s=737}
{x=163,m=20,a=746,s=795}
{x=2331,m=12,a=4,s=49}
{x=466,m=121,a=63,s=1424}
{x=635,m=1239,a=1074,s=519}
{x=954,m=372,a=648,s=1565}
{x=1508,m=102,a=2749,s=293}
{x=81,m=332,a=104,s=1926}
{x=3211,m=2227,a=899,s=1027}
{x=866,m=2067,a=564,s=256}
{x=681,m=2466,a=724,s=1192}
{x=425,m=2176,a=406,s=1763}
{x=72,m=946,a=115,s=1000}
{x=71,m=469,a=589,s=115}
{x=2161,m=173,a=707,s=2988}
{x=1580,m=2347,a=396,s=672}
{x=1503,m=271,a=59,s=324}
{x=2420,m=1038,a=217,s=2948}
{x=1784,m=196,a=2399,s=42}
{x=1097,m=1284,a=110,s=51}
{x=3122,m=1207,a=49,s=419}
{x=180,m=779,a=1846,s=138}
{x=734,m=1765,a=1674,s=831}
{x=266,m=25,a=20,s=1442}
{x=1783,m=369,a=2218,s=766}
{x=199,m=19,a=385,s=9}
{x=86,m=212,a=51,s=74}
{x=688,m=671,a=108,s=1025}
{x=1647,m=1964,a=94,s=2255}
{x=9,m=1553,a=466,s=511}
{x=17,m=409,a=411,s=708}
{x=215,m=337,a=213,s=1380}
{x=20,m=521,a=2612,s=1753}
{x=113,m=44,a=528,s=2022}
{x=1396,m=139,a=960,s=1355}
{x=2537,m=2042,a=1731,s=1287}
{x=300,m=1552,a=298,s=266}
{x=1449,m=266,a=711,s=755}
{x=448,m=11,a=1075,s=2561}
{x=863,m=2396,a=795,s=921}
{x=278,m=1351,a=1235,s=77}
{x=715,m=803,a=847,s=541}
{x=23,m=3078,a=501,s=42}
{x=1801,m=2452,a=973,s=2206}
{x=1511,m=392,a=2747,s=58}
{x=937,m=1197,a=619,s=468}
{x=1938,m=915,a=154,s=277}
{x=176,m=1129,a=171,s=509}
{x=140,m=1418,a=1834,s=576}
{x=503,m=545,a=2640,s=1237}
{x=2055,m=3326,a=141,s=2}
{x=177,m=965,a=69,s=508}
{x=47,m=361,a=1507,s=1463}
{x=1220,m=1580,a=1733,s=34}
{x=1816,m=705,a=1208,s=14}
{x=125,m=1578,a=511,s=495}
{x=328,m=172,a=2514,s=536}
{x=826,m=1399,a=588,s=1265}
{x=817,m=1535,a=80,s=17}
{x=129,m=642,a=136,s=619}
{x=1793,m=2369,a=2431,s=7}
{x=1707,m=382,a=2194,s=147}
{x=188,m=504,a=625,s=1200}
{x=113,m=2415,a=1774,s=1899}
{x=624,m=398,a=44,s=1465}
{x=1139,m=254,a=769,s=667}
{x=152,m=6,a=307,s=566}
{x=16,m=1022,a=491,s=299}
{x=1893,m=706,a=7,s=560}
{x=1309,m=647,a=268,s=1017}
{x=470,m=666,a=3080,s=201}
{x=1434,m=1297,a=105,s=1178}
{x=2941,m=651,a=903,s=1667}
{x=917,m=230,a=17,s=938}
{x=1819,m=347,a=30,s=2116}
{x=734,m=440,a=1760,s=203}
{x=31,m=321,a=126,s=607}
{x=1685,m=1380,a=1491,s=2853}
{x=127,m=1344,a=511,s=2273}
{x=1286,m=742,a=504,s=1217}
{x=1897,m=1684,a=181,s=2429}
{x=1168,m=549,a=1420,s=2295}
{x=485,m=1818,a=1715,s=1043}
{x=1590,m=2520,a=403,s=1694}
{x=493,m=3088,a=945,s=23}
{x=201,m=1021,a=406,s=358}
{x=475,m=2228,a=942,s=34}
{x=2569,m=117,a=1121,s=401}
{x=1342,m=187,a=318,s=619}
{x=307,m=717,a=752,s=407}
{x=27,m=3660,a=2557,s=2584}
{x=1827,m=592,a=89,s=1472}
{x=346,m=197,a=2899,s=1044}
{x=375,m=641,a=424,s=2181}
{x=456,m=400,a=96,s=782}
{x=221,m=975,a=1559,s=30}
{x=50,m=423,a=1902,s=2272}
{x=1542,m=480,a=496,s=888}
{x=1236,m=345,a=10,s=1654}
{x=42,m=392,a=800,s=656}
{x=789,m=42,a=392,s=641}
{x=1141,m=979,a=1581,s=1186}
{x=418,m=290,a=193,s=358}
{x=127,m=2879,a=1135,s=2318}
{x=886,m=356,a=6,s=3111}
{x=44,m=33,a=1345,s=3718}
{x=265,m=2086,a=1608,s=523}
{x=4,m=202,a=1814,s=1290}
{x=3089,m=266,a=438,s=1945}
{x=94,m=84,a=1480,s=778}
{x=1889,m=514,a=66,s=1715}
{x=2542,m=3329,a=507,s=1473}
{x=264,m=1950,a=1045,s=295}
{x=356,m=1479,a=479,s=610}
{x=35,m=2046,a=12,s=1138}
{x=643,m=623,a=5,s=1729}
{x=85,m=1026,a=1223,s=1474}
{x=145,m=1766,a=1872,s=27}
{x=352,m=251,a=1761,s=127}
{x=2810,m=1497,a=2690,s=1472}
{x=91,m=192,a=632,s=2}
{x=1075,m=104,a=372,s=423}
{x=345,m=1334,a=89,s=559}
{x=145,m=117,a=428,s=1215}
{x=1491,m=1643,a=286,s=61}
{x=1811,m=864,a=245,s=806}
{x=158,m=397,a=115,s=245}
{x=155,m=3337,a=389,s=1198}
{x=972,m=728,a=1262,s=2466}
{x=1822,m=1166,a=681,s=816}
{x=24,m=270,a=1509,s=241}
{x=2149,m=259,a=2187,s=880}
{x=1274,m=1312,a=513,s=143}
{x=632,m=1080,a=13,s=67}
{x=21,m=2680,a=2236,s=384}
{x=19,m=680,a=874,s=1306}
{x=252,m=1265,a=589,s=105}
{x=9,m=226,a=1061,s=159}
{x=669,m=682,a=889,s=82}
{x=44,m=264,a=370,s=893}
{x=303,m=1084,a=83,s=195}"""


@mark.parametrize(("input_string", "expected_output"), [(EXAMPLE_INPUT, 19114), (PUZZLE_INPUT, 333263)])
def test_part_workflow(input_string: str, expected_output: int) -> None:
    assert part_workflow(input_string) == expected_output


@mark.parametrize(
    ("input_string", "expected_output"), [(EXAMPLE_INPUT, 167409079868000), (PUZZLE_INPUT, 130745440937650)]
)
def test_part_workflow_combinations(input_string: str, expected_output: int) -> None:
    assert part_workflow_combinations(input_string) == expected_output