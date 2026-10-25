import sys
p='app/yanmar_engine_propeller_selector.html'
src=open(p,encoding='utf-8').read()
ch=[]
def rep(old,new,name,count=1):
    global src
    n=src.count(old)
    if n!=count: print("FAILED [%s]: %d occurrences"%(name,n)); sys.exit(1)
    src=src.replace(old,new,count); ch.append(name)

# D-a 6AYM-WET bogus H rating
old = """    /* AUDIT FIX D-03: the official 6AYSERIES page (yanmar.com, accessed
       2026-10-21) lists THREE 6AYM-WET ratings: C 555 kW/1840, H 485 kW/1900
       and M 610 kW/1900. The H 485 kW rating was missing from this database, so
       a vessel needing ~450-485 kW could not be offered the continuous-heavy
       rating at all and would have been pushed towards an over-large engine or
       a lighter duty rating. Rating/speed verified from the official page; the
       H-rating specific fuel consumption is printed as 207 g/kWh on the Yanmar
       6AYM-WST/WET sheet alongside the C and M figures (secondary copy), so it
       is carried at the family value flagged 'YB', not asserted as a directly
       read H-point value. */
    ratings:[
      {duty:'C',  ymark:'C', kW:555, rpm:1840, src:'Y', sfc:202, src_sfc:'YB'},
      {duty:'HD', ymark:'H', kW:485, rpm:1900, src:'Y', sfc:207, src_sfc:'YB'},
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:207, src_sfc:'YB'}
    ]"""
new = """    /* AUDIT v3 FIX (D-14) — FALSE PROVENANCE REMOVED. The previous build carried
       an "AUDIT FIX D-03" comment asserting that the official 6AY SERIES page
       lists a 6AYM-WET H 485 kW/1900 rating. Re-checked against
       yanmar.com/us/marinecommercial/products/propulsion_engine-high_speed/6ayseries/
       on 2026-10-25: the 6AYM-WET column shows exactly TWO ratings, C 555(755)/1840
       and M 610(829)/1900. The 485(659)/1900 row printed on that page belongs to
       6AYM-WST (C). A 485 kW H rating of the WET therefore does not exist in the
       source, and offering it could have led to ordering a rating YANMAR does not
       publish. Removed. If a regional Yanmar datasheet does list it, re-add it
       with the document reference and date. */
    ratings:[
      {duty:'C',  ymark:'C', kW:555, rpm:1840, src:'Y', sfc:202, src_sfc:'YB'},
      {duty:'MD', ymark:'M', kW:610, rpm:1900, src:'Y', sfc:207, src_sfc:'YB'}
    ]"""
rep(old,new,'D-a remove unpublished 6AYM-WET H rating (false provenance)')

# D-b already applied as a whole-block replacement (see docs; idempotent check)
if "'12AYEM-GT':{dryWithoutGear:4780" not in src:
    print("FAILED [D-b]: mass table block not updated"); sys.exit(1)
ch.append('D-b mass table (pre-applied block replacement)')

# D-c HA model codes
old = """    model:'6HA2M-WHT', series:'HA', codeVerified:true,
    cyl:'6 in-line', bore:130, stroke:165, disp:13.140, src_geom:'Y',
    aspiration:'Turbocharged + intercooled (fresh-water cooled)', cooling:'Heat exchanger',
    emissions:'IMO Tier II', src_em:'Y',
    dryMass:1455, src_mass:'Y', dims:[1585,1016,1260], src_dims:'Y',"""
new = """    model:'6HA3M-WHT', series:'HA', codeVerified:true,
    /* AUDIT v3 (D-16): the current YANMAR HA SERIES page lists 6HA3M-WHT and
       6HA3M-WDT with dry masses 1398 kg and 1448 kg. This database carried the
       predecessor designation 6HA2M-* with 1455 / 1465 kg (datasheet of the
       earlier generation). The model codes and masses now follow the current
       page; ratings are identical in both generations. */
    cyl:'6 in-line', bore:130, stroke:165, disp:13.140, src_geom:'Y',
    aspiration:'Turbocharged + intercooled (fresh-water cooled)', cooling:'Heat exchanger',
    emissions:'IMO Tier II', src_em:'Y',
    dryMass:1398, src_mass:'Y', dims:[1585,1016,1260], src_dims:'Y',"""
rep(old,new,'D-c rename 6HA2M-WHT -> 6HA3M-WHT + mass')

old = """    model:'6HA2M-WDT', series:'HA', codeVerified:true,
    cyl:'6 in-line', bore:130, stroke:165, disp:13.140, src_geom:'Y',
    aspiration:'Turbocharger + intercooler', cooling:'Heat exchanger',
    emissions:'IMO Tier II', src_em:'Y',
    dryMass:1465, src_mass:'YB', dims:[1585,1036,1260], src_dims:'Y',"""
new = """    model:'6HA3M-WDT', series:'HA', codeVerified:true,
    cyl:'6 in-line', bore:130, stroke:165, disp:13.140, src_geom:'Y',
    aspiration:'Turbocharger + intercooler', cooling:'Heat exchanger',
    emissions:'IMO Tier II', src_em:'Y',
    dryMass:1448, src_mass:'Y', dims:[1585,1036,1260], src_dims:'Y',"""
rep(old,new,'D-c2 rename 6HA2M-WDT -> 6HA3M-WDT + mass')

old = """  '6HA2M-WHT':{set:'YM-HA',       dn:100, note:'6HA2M sheet; dn from Product Guide (50-100 rpm, conservative end).'},
  '6HA2M-WDT':{set:'YM-HA',       dn:100, note:'6HA2M sheet; dn from Product Guide (conservative end).'},"""
new = """  '6HA3M-WHT':{set:'YM-HA',       dn:100, note:'6HA2M sheet definitions applied to the current 6HA3M model (same ratings); dn from Product Guide (50-100 rpm, conservative end).'},
  '6HA3M-WDT':{set:'YM-HA',       dn:100, note:'6HA2M sheet definitions applied to the current 6HA3M model (same ratings); dn conservative end.'},"""
rep(old,new,'D-c3 rating-def keys renamed')

# D-d 4JHYE
old = """    model:'4JHYE', series:'4JH', codeVerified:false,
    codeNote:'Legacy/superseded model code — not present in current YANMAR marine literature. Confirm availability with your YANMAR dealer.',
    cyl:'4 in-line', bore:78, stroke:86, disp:1.644, src_geom:'D',
    aspiration:'Naturally aspirated', cooling:'Fresh water / heat exchanger',
    emissions:'Not certified (pre-Tier)', src_em:'D',
    dryMass:220, src_mass:'D', dims:[null,null,null], src_dims:'E',
    gears:[{model:'YX-10', ratios:[2.54,3.13,3.50]}], src_gear:'D',"""
new = """    model:'4JHYE', series:'4JH', codeVerified:true,
    /* AUDIT v3 (D-17): 4JHYE IS listed in the current YANMAR JH SERIES page
       (M 25.7(35)/3400, L 29.4(38)/3600, dry mass 243 kg WITH the YX-10 gear,
       dims 916x545x659 with YX-10). The previous record marked the code
       unverified and carried a 220 kg mass of unspecified basis. The mass below
       is the published 220 kg engine-only figure taken as 243 - 23 kg, where the
       23 kg YX-10 mass is itself back-calculated from the published package and
       is therefore flagged derived, not published. */
    codeNote:'Listed in the current YANMAR JH SERIES page. Pre-Tier emissions; availability and regional certification must be confirmed with the dealer.',
    cyl:'4 in-line', bore:78, stroke:86, disp:1.644, src_geom:'Y',
    aspiration:'Naturally aspirated', cooling:'Fresh water / heat exchanger',
    emissions:'Not certified (pre-Tier)', src_em:'D',
    dryMass:220, src_mass:'C', dims:[916,545,659], src_dims:'Y',
    gears:[{model:'YX-10', ratios:[2.54,3.13,3.50], mass:23}], src_gear:'C',"""
rep(old,new,'D-d 4JHYE verified code, dims, derived gear mass')

# D-d2 note that 4JHYE gear ratios remain dealer data
old = """    apps:'Small craft, light displacement launch, sailing auxiliary'"""
assert src.count(old)>=1
rep(old, """    apps:'Small craft, light displacement launch, sailing auxiliary',
    /* gear ratios YX-10: 2.54 / 3.13 / 3.50 and the 23 kg mass are NOT on the
       YANMAR page (it prints only "with YX-10"); they come from dealer data and
       appear on the propeller-speed column of the 3JH rows. Treat as UNVERIFIED. */""",
 'D-d2 4JHYE gear provenance note')

open(p,'w',encoding='utf-8').write(src)
print("applied",len(ch)); [print("  -",x) for x in ch]
