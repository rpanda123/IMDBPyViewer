tilde_mode(regression).
sampling_strategy(fixed(15000)).
%outerloop(queries).
%use_packs(0).
typed_language(yes).
type(rating(movie,number)).
predict(rating(+,-)).
minimal_cases(10).
%discretize(equal_freq).

type(threshold_admissions(number)).
type(admissionsInf(movie,number,number,number,country)).
type(admissionsSup(movie,number,number,number,country)).
rmode(#(Threshold: threshold_admissions(Threshold), admissionsInf(+Key,+-Tickets2,Threshold,-Duration,-Country))).
rmode(#(Threshold: threshold_admissions(Threshold), admissionsSup(+Key,+-Tickets2,Threshold,-Duration,-Country))).

type(threshold_votes(number)).
type(votesInf(movie,number)).
type(votesSup(movie,number)).
rmode(#(Threshold: threshold_votes(Threshold), votesInf(+Movie,Threshold))).
rmode(#(Threshold: threshold_votes(Threshold), votesSup(+Movie,Threshold))).

type(a_genre(Genre)).
type(genre(movie,genre)).
rmode(#(Genre: a_genre(Genre), genre(+Movie,Genre))).
type(a_countrytrue(countrytrue)).
type(country(movie,countrytrue)).
rmode(#(CountryTrue: a_countrytrue(CountryTrue), country(+Movie,CountryTrue))).

type(a_country(country)).
type(distributor_country(movie,country)).
rmode(#(C: a_country(C), distributor_country(+M,C))).
type(production_country(movie,country)).
rmode(#(C: a_country(C), production_country(+M,C))).
type(special_effects_country(movie,country)).
rmode(#(C: a_country(C), special_effects_country(+M,C))).
type(miscellaneous_country(movie,country)).
rmode(#(C: a_country(C), miscellaneous_country(+M,C))).

%type(aspect_ratio(movie,aspect_ratio,extra)).
%rmode(aspect_ratio(+,#,-)).

type(a_name(name)).
type(distributor_name(movie,name)).
rmode(#(N: a_name(N), distributor_name(+M,N))).
type(production_name(movie,name)).
rmode(#(N: a_name(N), production_name(+M,N))).
type(special_effects_name(movie,name)).
rmode(#(N: a_name(N), special_effects_name(+M,N))).
type(miscellaneous_name(movie,name)).
rmode(#(N: a_name(N), miscellaneous_name(+M,N))).

type(language(movie,language)).
rmode(language(+,#)).

%type(director(movie,person)).
%rmode(director(+,#)).
%type(gender_director(movie,gender)).
%rmode(gender_director(+,#)).

%type(cast(movie,person,importance)).
%rmode(cast(+,#,#)).
%type(producer(movie,person)).
%rmode(producer(+,#)).
%type(writer(movie,person)).
%rmode(writer(+,#)).

type(a_season(season)).
type(release_season(movie,countrytrue,season)).
rmode(#((C,S): (a_countrytrue(C), a_season(S)), release_season(+M,C,S))).

type(a_rating(rating)).
type(certificate(movie,countrytrue,rating)).
rmode(#((C,R): (a_countrytrue(C), a_rating(R)), certificate(+M,C,R))).

type(follows(movie,movie)).
type(followed_by(movie,movie)).
rmode(follows(+,-)).
rmode(followed_by(+,-)).

type(references(movie,movie)).
type(referenced_in(movie,movie)).
rmode(references(+,-)).
rmode(referenced_in(+,-)).

type(remake_of(movie,movie)).
type(remade_as(movie,movie)).
rmode(remake_of(+,-)).
rmode(remade_as(+,-)).

type(spoofs(movie,movie)).
type(spoofed_in(movie,movie)).
rmode(spoofs(+,-)).
rmode(spoofed_in(+,-)).

type(features(movie,movie)).
type(featured_in(movie,movie)).
rmode(features(+,-)).
rmode(featured_in(+,-)).

type(spin_off_from(movie,movie)).
type(spin_off(movie,movie)).
rmode(spin_off_from(+,-)).
rmode(spin_off(+,-)).

type(version_of(movie,movie)).
type(similar_to(movie,movie)).
rmode(version_of(+,-)).
rmode(similar_to(+,-)).

type(edited_into(movie,movie)).
type(edited_from(movie,movie)).
rmode(edited_into(+,-)).
rmode(edited_from(+,-)).

type(alternate_language_version_of(movie,movie)).
rmode(alternate_language_version_of(+,-)).
type(unknown_link(movie,movie)).
rmode(unknown_link(+,-)).

type(a_keyword(keyword)).
type(keywords(movie,keyword)).
rmode(#(Keyword: a_keyword(Keyword), keywords(+Key,Keyword))).
type(a_couple_color(color,extra2)).
type(color_info(movie,color,extra2)).
rmode(#((Color,Extra): a_couple_color(Color,Extra), color_info(+Key,Color,Extra))).
type(a_couple_sound(sound,extra3)).
type(sound_mix(movie,sound,extra3)).
rmode(#((Sound,Extra): a_couple_sound(Sound,Extra), sound_mix(+Key,Sound,Extra))).


