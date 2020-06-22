(* using http://caml.inria.fr/pub/docs/manual-camlp4/index.html *)
let rec lex = parser
	(* skip any whitespace. *)
	| [< ' (' ' | '\n' | '\r' | '\t'); stream >] -> lex stream
	(* identifier: [a-zA-Z][a-zA-Z0-9] *)
	| [< ' ('A' .. 'Z' | 'a' .. 'z' as c); stream >] ->
		let buffer = Buffer.create 1 in
		Buffer.add_char buffer c;
		lex_ident buffer stream
	(* number: [0-9]+ *)
	| [< ' ('0' .. '9' as c); stream >] ->
		let buffer = Buffer.create 1 in
		Buffer.add_char buffer c;
		lex_number buffer stream
	(* comments *)
	| [< ' ('#'); stream >] ->
		lex_comment stream
	(* otherwise, operator or end of file so return ascii *)
	| [< 'c; stream >] ->
		[< 'Token.Kwd c; lex stream >]	
	(* end of stream *)
	| [< >] -> [< >]

(* parse the rest of the identifier and check against our keywords *)
and lex_ident buffer = parser
	| [< ' ('A' .. 'Z' | 'a' .. 'z' | '0' .. '9' as c); stream >] ->
		Buffer.add_char buffer c;
		lex_ident buffer stream
	| [< stream=lex >] ->
		match Buffer.contents buffer with
		| "def" -> [< 'Token.Def; stream >]
		| "extern" -> [< 'Token.Extern; stream >]
		| id -> [< 'Token.Ident id; stream >]

(* mutually recursive helper for numbers including floats,  this isn’t doing sufficient error checking: it will raise Failure if the string “1.23.45.67”. *)
and lex_number buffer = parser
	| [< ' ('0' .. '9' | '.' as c); stream >] ->
		Buffer.add_char buffer c;
		lex_number buffer stream
	| [< stream=lex >] ->
		[< 'Token.Number (float_of_string (Buffer.contents buffer)); stream >]

(* handle comment by skipping to end of line and returning the character after *)
and lex_comment = parser
	| [< ' ('\n'); stream=lex >] -> stream
	| [< 'c; e=lex_comment >] -> e
	| [< >] -> [< >]
