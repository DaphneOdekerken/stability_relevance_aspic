literal(q1).
literal(q2).
literal(q3).
literal(q4).
literal(q5).
literal(q6).
literal(q7).
literal(q8).
literal(q9).
literal(q10).
literal(q11).
literal(q12).
literal(q13).
literal(q14).
literal(q15).
literal(not_q1).
literal(not_q2).
literal(not_q3).
literal(not_q4).
literal(not_q5).
literal(not_q6).
literal(not_q7).
literal(not_q8).
literal(not_q9).
literal(not_q10).
literal(not_q11).
literal(not_q12).
literal(not_q13).
literal(not_q14).
literal(not_q15).
literal(fraudarticle326).
literal(not_fraudarticle326).
literal(fraudarticle326e).
literal(not_fraudarticle326e).
literal(fraudarticle326expertcheckrequired).
literal(not_fraudarticle326expertcheckrequired).
literal(fraudarticle326eexpertcheckrequired).
literal(not_fraudarticle326eexpertcheckrequired).
literal(civilcase).
literal(not_civilcase).
literal(presumablyfraud).
literal(not_presumablyfraud).
literal(presumablyforgery).
literal(not_presumablyforgery).
literal(expertcheckrequired).
literal(not_expertcheckrequired).
literal(deliverymaystillcome).
literal(not_deliverymaystillcome).
literal(complainantreceivednothing).
literal(not_complainantreceivednothing).
literal(complainantreceivedbrokenproduct).
literal(not_complainantreceivedbrokenproduct).
literal(complainantreceivedfakeproduct).
literal(not_complainantreceivedfakeproduct).
literal(rejectcomplaint).
literal(not_rejectcomplaint).
literal(refertohallmarkcompany).
literal(not_refertohallmarkcompany).
literal(webshoponsomewhitelist).
literal(not_webshoponsomewhitelist).

queryable(q1).
queryable(q2).
queryable(q3).
queryable(q4).
queryable(q5).
queryable(q6).
queryable(q7).
queryable(q8).
queryable(q9).
queryable(q10).
queryable(q11).
queryable(q12).
queryable(q13).
queryable(q14).
queryable(q15).
queryable(not_q1).
queryable(not_q2).
queryable(not_q3).
queryable(not_q4).
queryable(not_q5).
queryable(not_q6).
queryable(not_q7).
queryable(not_q8).
queryable(not_q9).
queryable(not_q10).
queryable(not_q11).
queryable(not_q12).
queryable(not_q13).
queryable(not_q14).
queryable(not_q15).

neg(fraudarticle326,not_fraudarticle326).
neg(fraudarticle326e,not_fraudarticle326e).
neg(fraudarticle326expertcheckrequired,not_fraudarticle326expertcheckrequired).
neg(fraudarticle326eexpertcheckrequired,not_fraudarticle326eexpertcheckrequired).
neg(civilcase,not_civilcase).
neg(q1,not_q1).
neg(q2,not_q2).
neg(q2,not_q4).
neg(q2,q5).
neg(q3,not_q3).
neg(q4,not_q4).
neg(q5,not_q4).
neg(q5,q2).
neg(q5,not_q5).
neg(q6,not_q6).
neg(q7,q13).
neg(q7,not_q7).
neg(q7,not_q6).
neg(q8,not_q8).
neg(q9,not_q9).
neg(q10,not_q14).
neg(q10,not_q10).
neg(q11,not_q14).
neg(q11,not_q11).
neg(q11,not_q10).
neg(q12,not_q12).
neg(presumablyfraud,not_presumablyfraud).
neg(presumablyforgery,not_presumablyforgery).
neg(expertcheckrequired,not_expertcheckrequired).
neg(q13,q7).
neg(q13,not_q13).
neg(q13,not_q6).
neg(q14,not_q14).
neg(deliverymaystillcome,not_deliverymaystillcome).
neg(complainantreceivednothing,not_complainantreceivednothing).
neg(complainantreceivedbrokenproduct,not_complainantreceivedbrokenproduct).
neg(complainantreceivedfakeproduct,not_complainantreceivedfakeproduct).
neg(rejectcomplaint,not_rejectcomplaint).
neg(q15,not_q15).
neg(q15,not_q6).
neg(refertohallmarkcompany,not_refertohallmarkcompany).
neg(webshoponsomewhitelist,not_webshoponsomewhitelist).

neg(not_fraudarticle326,fraudarticle326).
neg(not_fraudarticle326e,fraudarticle326e).
neg(not_fraudarticle326expertcheckrequired,fraudarticle326expertcheckrequired).
neg(not_fraudarticle326eexpertcheckrequired,fraudarticle326eexpertcheckrequired).
neg(not_civilcase,civilcase).
neg(not_q1,q1).
neg(not_q2,q2).
neg(not_q4,q2).
neg(q5,q2).
neg(not_q3,q3).
neg(not_q4,q4).
neg(not_q4,q5).
neg(q2,q5).
neg(not_q5,q5).
neg(not_q6,q6).
neg(q13,q7).
neg(not_q7,q7).
neg(not_q6,q7).
neg(not_q8,q8).
neg(not_q9,q9).
neg(not_q14,q10).
neg(not_q10,q10).
neg(not_q14,q11).
neg(not_q11,q11).
neg(not_q10,q11).
neg(not_q12,q12).
neg(not_presumablyfraud,presumablyfraud).
neg(not_presumablyforgery,presumablyforgery).
neg(not_expertcheckrequired,expertcheckrequired).
neg(q7,q13).
neg(not_q13,q13).
neg(not_q6,q13).
neg(not_q14,q14).
neg(not_deliverymaystillcome,deliverymaystillcome).
neg(not_complainantreceivednothing,complainantreceivednothing).
neg(not_complainantreceivedbrokenproduct,complainantreceivedbrokenproduct).
neg(not_complainantreceivedfakeproduct,complainantreceivedfakeproduct).
neg(not_rejectcomplaint,rejectcomplaint).
neg(not_q15,q15).
neg(not_q6,q15).
neg(not_refertohallmarkcompany,refertohallmarkcompany).
neg(not_webshoponsomewhitelist,webshoponsomewhitelist).

body(0,presumablyforgery).
body(0,presumablyfraud).
head(0,fraudarticle326).
body(1,presumablyfraud).
head(1,fraudarticle326e).
body(2,presumablyforgery).
body(2,presumablyfraud).
head(2,not_fraudarticle326e).
body(3,expertcheckrequired).
head(3,fraudarticle326eexpertcheckrequired).
body(4,expertcheckrequired).
body(4,presumablyforgery).
head(4,not_fraudarticle326eexpertcheckrequired).
body(5,expertcheckrequired).
body(5,presumablyforgery).
head(5,fraudarticle326expertcheckrequired).
body(6,not_deliverymaystillcome).
body(6,not_q4).
body(6,q1).
body(6,q3).
head(6,complainantreceivednothing).
body(7,q1).
body(7,q2).
body(7,q3).
body(7,q4).
head(7,complainantreceivedfakeproduct).
body(8,not_q2).
body(8,not_q5).
body(8,q1).
body(8,q3).
body(8,q4).
head(8,complainantreceivedbrokenproduct).
body(9,complainantreceivednothing).
head(9,civilcase).
body(10,complainantreceivednothing).
head(10,presumablyfraud).
body(11,complainantreceivedbrokenproduct).
head(11,civilcase).
body(12,complainantreceivedbrokenproduct).
head(12,expertcheckrequired).
body(13,complainantreceivedfakeproduct).
head(13,civilcase).
body(14,complainantreceivedfakeproduct).
head(14,presumablyfraud).
body(15,webshoponsomewhitelist).
body(15,q6).
head(15,not_presumablyfraud).
body(16,webshoponsomewhitelist).
body(16,q6).
head(16,not_expertcheckrequired).
body(17,q8).
head(17,presumablyforgery).
body(18,q10).
body(18,q11).
head(18,presumablyforgery).
body(19,q9).
head(19,presumablyforgery).
body(20,q13).
body(20,q6).
head(20,presumablyforgery).
body(21,not_q14).
body(21,not_q4).
head(21,not_deliverymaystillcome).
body(22,not_q4).
body(22,q12).
body(22,q14).
head(22,not_deliverymaystillcome).
body(23,q13).
body(23,q6).
head(23,not_deliverymaystillcome).
body(24,q15).
body(24,q6).
head(24,not_civilcase).
body(25,complainantreceivednothing).
body(25,q15).
body(25,q6).
head(25,refertohallmarkcompany).
body(26,complainantreceivedbrokenproduct).
body(26,q15).
body(26,q6).
head(26,refertohallmarkcompany).
body(27,complainantreceivedfakeproduct).
body(27,q15).
body(27,q6).
head(27,refertohallmarkcompany).
body(28,q6).
body(28,q7).
head(28,webshoponsomewhitelist).
body(29,q15).
body(29,q6).
head(29,webshoponsomewhitelist).
body(30,q5).
head(30,rejectcomplaint).
body(31,not_q1).
head(31,rejectcomplaint).
body(32,not_q3).
head(32,rejectcomplaint).
body(33,webshoponsomewhitelist).
body(33,q6).
head(33,rejectcomplaint).
body(34,not_q12).
body(34,not_q4).
body(34,webshoponsomewhitelist).
body(34,q11).
head(34,rejectcomplaint).
body(35,not_q12).
body(35,not_q4).
body(35,webshoponsomewhitelist).
body(35,q10).
head(35,rejectcomplaint).
body(36,not_q12).
body(36,not_q4).
body(36,webshoponsomewhitelist).
body(36,q14).
head(36,rejectcomplaint).
body(37,not_q12).
body(37,not_q13).
body(37,not_q4).
body(37,q11).
body(37,q6).
head(37,rejectcomplaint).
body(38,not_q12).
body(38,not_q4).
body(38,not_q6).
body(38,q11).
head(38,rejectcomplaint).
body(39,not_q12).
body(39,not_q13).
body(39,not_q4).
body(39,q10).
body(39,q6).
head(39,rejectcomplaint).
body(40,not_q12).
body(40,not_q4).
body(40,not_q6).
body(40,q10).
head(40,rejectcomplaint).
body(41,not_q12).
body(41,not_q13).
body(41,not_q4).
body(41,q14).
body(41,q6).
head(41,rejectcomplaint).
body(42,not_q12).
body(42,not_q4).
body(42,not_q6).
body(42,q14).
head(42,rejectcomplaint).

preferred(0,0).
preferred(1,1).
preferred(2,2).
preferred(3,3).
preferred(4,4).
preferred(5,5).
preferred(6,6).
preferred(7,7).
preferred(8,8).
preferred(9,9).
preferred(10,10).
preferred(11,11).
preferred(12,12).
preferred(13,13).
preferred(14,14).
preferred(15,15).
preferred(16,16).
preferred(17,17).
preferred(18,18).
preferred(19,19).
preferred(20,20).
preferred(21,21).
preferred(22,22).
preferred(23,23).
preferred(24,24).
preferred(25,25).
preferred(26,26).
preferred(27,27).
preferred(28,28).
preferred(29,29).
preferred(30,30).
preferred(31,31).
preferred(32,32).
preferred(33,33).
preferred(34,34).
preferred(35,35).
preferred(36,36).
preferred(37,37).
preferred(38,38).
preferred(39,39).
preferred(40,40).
preferred(41,41).
preferred(42,42).

topic(fraudarticle326).