"""Independent arithmetic and real SQL witnesses for the revised study cases."""
from pathlib import Path
import json,math,sqlite3,statistics
ROOT=Path(__file__).resolve().parents[1]
tests=[t for i in range(1,5) for t in json.loads((ROOT/f'test-packs/revised-{i}.json').read_text())['tests']]
def question(test,objective):return next(q for t in tests if t['id']==test for q in t['questions'] if q['objective']==objective)
def required(test,objective,text):
 q=question(test,objective);assert any(o['correct'] and o['text']==text for o in q['options']),(q['id'],text)
def rmse(actual,predicted):return math.sqrt(sum((a-b)**2 for a,b in zip(actual,predicted))/len(actual))
for test,objective,values in [('T23','Mean median mode',[2,4,4,6,9]),('T35','Summary calculation',[1,2,2,5,10]),('T49','Capacity summaries',[3,4,4,7,12])]:
 required(test,objective,f'The mean is {statistics.mean(values):g} days')
 required(test,objective,f'The median is {statistics.median(values):g} days')
 required(test,objective,f'The mode is {statistics.mode(values):g} days')
assert statistics.median([2,4,4,6,90])==4 and statistics.mean([2,4,4,6,90])!=5
required('T18','Completeness denominator',f'Field completeness is {180/200*100:g}% for these records')
required('T48','Missing-date comparison',f'Overall closure-date completeness is {950/1000*100:g}%')
required('T39','Proportions',f'Their complaint rates are {10/100*100:g}% and {20/1000*100:g}% using those denominators')
assert math.isclose(rmse([30,40],[32,36]),math.sqrt(10)) and math.isclose(rmse([30,40],[30,30]),math.sqrt(50))
required('T38','RMSE calculation',f'Candidate RMSE is sqrt(10), about {rmse([30,40],[32,36]):.3f}')
required('T38','RMSE calculation',f'Baseline RMSE is sqrt(50), about {rmse([30,40],[30,30]):.3f}')
required('T49','Common holdout',f'Candidate RMSE is {rmse([10,14],[12,12]):g}')
required('T49','Common holdout',f'Baseline RMSE is sqrt(8), about {rmse([10,14],[10,10]):.3f}')
assert .04>.01 and .03<.05
required('T49','Planned threshold','Do not reject the null at the planned threshold')
required('T35','Planned inferential decision','Reject the stated null at the planned threshold')
db=sqlite3.connect(':memory:');db.executescript('CREATE TABLE requests(id INTEGER PRIMARY KEY, service TEXT); CREATE TABLE lookup(service TEXT);')
db.executemany('INSERT INTO requests VALUES (?,?)',enumerate(['A','A','B','C'],1));db.executemany('INSERT INTO lookup VALUES (?)',[(x,) for x in ['A','A','B']])
assert db.execute('SELECT COUNT(*) FROM requests r LEFT JOIN lookup l ON r.service=l.service').fetchone()[0]==6
assert db.execute('SELECT COUNT(*) FROM requests r INNER JOIN lookup l ON r.service=l.service').fetchone()[0]==5
assert db.execute('SELECT COUNT(*) FROM requests r LEFT JOIN lookup l ON r.service=l.service WHERE l.service IS NULL').fetchone()[0]==1
required('T33','Row inflation arithmetic','The joined output has six rows')
required('T33','Row inflation arithmetic','One request has no lookup match')
db.executescript('DELETE FROM requests; DELETE FROM lookup;')
db.executemany('INSERT INTO requests VALUES (?,?)',[(i,str(i)) for i in range(1,81)])
# Two different multiplicity distributions witness the same row inflation.
for extras in [[str(i) for i in range(1,17)],[str(i) for i in range(1,9) for _ in range(2)]]:
 db.execute('DELETE FROM lookup');db.executemany('INSERT INTO lookup VALUES (?)',[(str(i),) for i in range(1,78)]+[(i,) for i in extras])
 assert db.execute('SELECT COUNT(*) FROM requests r LEFT JOIN lookup l ON r.service=l.service').fetchone()[0]==96
 assert db.execute('SELECT COUNT(*),COUNT(DISTINCT r.id) FROM requests r INNER JOIN lookup l ON r.service=l.service').fetchone()==(93,77)
required('T20','Join multiplication','An inner join on the same condition would have 93 rows')
required('T20','Join multiplication','The matched output represents 77 distinct request IDs')
arrays=[[1,2],[],[3,4,5]];assert sum(map(len,arrays))==5 and sum(bool(a) for a in arrays)==2
required('T29','Nested expansion','The expanded table contains five order rows')
required('T29','Nested expansion','Two customer IDs appear in the order rows')
print('Independent summaries, completeness/rates, p-value decisions, RMSE, nested expansion and real SQLite join witnesses passed.')
