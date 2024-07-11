literal(similar_url).
literal(not_similar_url).
literal(too_cheap).
literal(not_too_cheap).
literal(trusted).
literal(not_trusted).
literal(typosquatting).
literal(not_typosquatting).
literal(deception).
literal(not_deception).

queryable(similar_url).
queryable(not_similar_url).
queryable(too_cheap).
queryable(not_too_cheap).
queryable(trusted).
queryable(not_trusted).
queryable(typosquatting).
queryable(not_typosquatting).

axiom(similar_url).

neg(similar_url,not_similar_url).
neg(not_similar_url,similar_url).
neg(too_cheap,not_too_cheap).
neg(not_too_cheap,too_cheap).
neg(trusted,not_trusted).
neg(not_trusted,trusted).
neg(typosquatting,not_typosquatting).
neg(not_typosquatting,typosquatting).
neg(deception,not_deception).
neg(not_deception,deception).

head(d0,typosquatting).
body(d0,similar_url).
head(d1,deception).
body(d1,too_cheap).
head(d2,not_deception).
body(d2,trusted).

preferred(d0,d0).
preferred(d1,d1).
preferred(d2,d2).