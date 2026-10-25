P='app/yanmar_engine_propeller_selector.html'
s=open(P,encoding='utf-8').read(); orig=s
def rep(old,new,n=1):
    global s
    assert s.count(old)==n, (s.count(old), old[:80])
    s=s.replace(old,new)

rep("""function holtropPropulsion(p, D, EAR, PD, nProps){
  if(p.formK == null || p.Cf == null || p.Ca == null){ p = Object.assign({}, p, holtrop(p)); }""",
"""function holtropPropulsion(p, D, EAR, PD, nProps){
  /* AUDIT v3 FIX (H-03): this function needs the HULL INPUT object (or one
     carrying formK/Cf/Ca plus the hull form), not the object returned by
     holtrop(). The result of holtrop() does not repeat Cp/Cm/Cwp/lcb, so
     passing it silently produced w = t = eta_R = NaN and a NaN brake power.
     Refuse instead. */
  const need = ['Lwl','B','T','vol','Cp','Cm','Cwp','lcb'];
  const missing = need.filter(function(k){ return p == null || !isNum(p[k]); });
  if(missing.length)
    return {error:'holtropPropulsion requires the hull input object with ' + missing.join(', ') +
      ' (it was given a holtrop() RESULT, which does not repeat those fields). ' +
      'Pass the original input with formK/Cf/Ca, or the input object alone and let the function compute them.'};
  if(p.formK == null || p.Cf == null || p.Ca == null){ p = Object.assign({}, p, holtrop(p)); }""")
open(P,'w',encoding='utf-8').write(s)
print('patched +%d' % (len(s)-len(orig)))
