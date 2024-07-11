literal(q0).
literal(not_q0).
literal(q1).
literal(not_q1).
literal(q2).
literal(not_q2).
literal(a).
literal(not_a).

queryable(q0).
queryable(not_q0).
queryable(q1).
queryable(not_q1).
queryable(q2).
queryable(not_q2).

axiom(q0).
axiom(q1).

neg(q0,not_q0).
neg(not_q0,q0).
neg(q1,not_q1).
neg(not_q1,q1).
neg(q2,not_q2).
neg(not_q2,q2).
neg(a,not_a).
neg(not_a,a).

head(d0,a).
body(d0,q0).
head(d1,not_a).
body(d1,q1).
head(d2,not_a).
body(d2,q2).

preferred(d0,d0).
preferred(d0,d1).
preferred(d1,d1).
preferred(d2,d2).

topic(a).