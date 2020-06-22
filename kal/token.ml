(* attempt at https://llvm.org/docs/tutorial/OCamlLangImpl1.html *)
(* The lexer returns these 'kwd' if it is an unknown character, otherwise one of these others for known things. *)
type token = 
	(* commands *)
	| Def | Extern

	(* primary *)
	| Ident of string | Number of float

	(* unknown *)
	| Kwd of char

