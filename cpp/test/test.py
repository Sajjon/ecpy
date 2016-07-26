from ecpy.native import *
from ecpy import *
import time
import sys

Px1, Px2 = 4337918138942686854958542230148644189053704690003904437751560202817402049169239586648933175380231080067607459721048355942219823013518769899380883916254009, 5264396776927521465809520303908998560539265049775007823792483921039094484977406753852806697559554042789147024336762490917481809601429825340609194302098527
Py1, Py2 = 4155828099454307088035907810564030659210141681665165330160079570511033042779115531327485209386008020783026027466945845625648623223948015031775335216309267, 5425408530038263897744809400953990859117057287850392743244009500128107356544736059571998618592414772507555820486857590805428344257116831448362945079352076

Qx1, Qx2 = (5889626150551240372512653431010429611159784115110030339825196026379785410616730578506858093539305274403609491856684199747721361661558153344134767409402521, 623372711396686963252251532266402070840143991342848940374145445691562271772468387664916359653728440142716922426357801819835135182345249651829170759193237)
Qy1, Qy2 = (10438501200118030687430536952247522936721445659728153895410543029498510690234812688243662789844376022754642443267529844991498461534397875149568109885310206, 4784864196924457744891660113250965325160489070022384131861444729181295065486069592293866622436578883070132497189568957501507524793764966978094575997462727)
Qz1, Qz2 = (3044170762731299847052118583445230122358075951625628793615999346289303533079880771447680057754346597136518070995192889029816289471703634947670225918975114, 2980940984997360328281484262091884849433971390409088276791537941939855329427817618055544298222995249732927243472511363124269916586861038833419970278559519)

line_coeff_val = (10639604326234192062743631919883394572388165200931519828014733226965938211669864240337640177887972609617640356297590528965525200881158266103102530859289003, 5807169577012414010606700675857009134680645514659554085176364409970819126236954049036912375247178087174678139817374478908900472320452591987653540386856483)

ac_count = 0
wa_count = 0

def _assert(a, b, msg, cond):
  global ac_count, wa_count
  msg = msg.ljust(16)
  print ("[+] %s..." % (msg)).ljust(30),
  var = {"a": a, "b": b}
  if eval("a %s b" % cond, var):
    r = repr(b)[:64] + "..."
    print "\x1b[33m[  OK  ]\x1b[0m %s" % (r, )
    ac_count += 1
  else:
    print "\x1b[31m[ Fail ]\x1b[0m Expected: %r, Result: %r" % (b, a)
    wa_count += 1

def assert_neq(a, b, m):
  _assert(a, b, m, "!=")

def assert_eq(a, b, m):
  _assert(a, b, m, "==")

def main():
  ZZ = ZZ_create
  x = ZZ(2)
  y = ZZ(8)
  a = ZZ(12345)
  b = ZZ(331)
  c = ZZ(1001)
  d = ZZ(9907)
  assert_eq(x+y, ZZ(10), "x+y")
  assert_eq(x-y, ZZ(-6), "x-y")
  assert_eq(x*y, ZZ(16), "x*y")
  assert_eq(y/x, ZZ(4), "y/x")
  assert_eq(modinv(7, 65537), 18725, "modinv(7, 65537)")
  assert_eq(legendre(a, b), -1, "(12345|331) = -1")
  assert_eq(jacobi(c, d), -1, "(1001|9907) = -1")

  FF = lambda x: FF_create(x, p)
  p = 31
  x = FF(25)
  y = FF(41)
  assert_eq(y, FF(10), "y modulo check")
  assert_eq(x+y, FF(4), "x+y")
  assert_eq(x-y, FF(15), "x-y")
  assert_eq(x*y, FF(2), "x*y")
  assert_eq(x/y, FF(18), "x/y")

  modulo = 7
  EF = lambda x, y: EF_create(x, y, modulo, "x^2+1")
  x = EF(3, 0)
  y = EF(0, 5)
  assert_eq(x+y, EF(3, 5), "x+y")
  assert_eq(-x, EF(4, 0), "-x")
  assert_eq(x*y, EF(0, 1), "x*y")

  modulo = 41
  EF = lambda x, y: EF_create(x, y, modulo, "x^2+x+1")
  x = EF(61, 0)
  y = EF(0, 20)
  assert_eq(x, EF(20, 0), "x modulo check")
  assert_eq(x+y, EF(20, 20), "x+y")
  assert_eq(-x, EF(21, 0), "-x")
  assert_eq(x*y, EF(0, 31), "x*y")
  assert_eq(y.inv(), EF(2, 2), "1/y")

  p = 11093300438765357787693823122068501933326829181518693650897090781749379503427651954028543076247583697669597230934286751428880673539155279232304301123931419
  E = EC_create(0, 1, "EF")
  print E
  EF = lambda x1,x2,y1,y2,z1,z2: EP_EF_create(E, x1, x2, y1, y2, z1, z2, p, "x^2+x+1")
  P = EF(Px1, Px2, Py1, Py2, 1, 0)
  Q = EF(Qx1, Qx2, Qy1, Qy2, Qz1, Qz2)
  assert_eq(P.tuple(), ((Px1, Px2), (Py1, Py2), (1, 0)), "P.tuple()")
  assert_eq(Q.tuple(), ((Qx1, Qx2), (Qy1, Qy2), (Qz1, Qz2)), "P.tuple()")
  assert_eq(P * 123456789, Q, "123456789P")
  assert_eq(P.line_coeff(Q).tuple(), line_coeff_val, "line_coeffs")
  print "[+] %d Test(s) finished. %d Test(s) success, %d Test(s) fail." % (
        ac_count + wa_count, ac_count, wa_count)
  sys.exit(wa_count)

if __name__ == "__main__":
  main()
