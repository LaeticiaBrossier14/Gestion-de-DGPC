const SCENARIOS = [
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "RN12, Adekar",
    id: "SYN_accident_pedestrian_001__00001",
    turns: [
      { role: "caller", text: "allo 7imaya l'madaniya?" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, dachu yellan?" },
      { role: "caller", text: "azlemd! yiwen amghar thewthit tomobil di rn12, adekar! ighli, idukh, ul it-respirer-ara!" },
      { role: "operator", text: "sh7al n l'blessés?" },
      { role: "caller", text: "yiwen! 3ajlem!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amizour",
    id: "SYN_accident_pedestrian_001__00002",
    turns: [
      { role: "caller", text: "allo, arwa7u s zerb!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu llan?" },
      { role: "caller", text: "tomobil theqleb ameddak dagi amizour! ighli, idukh chwiya!" },
      { role: "operator", text: "d'accord, iwen kan?" },
      { role: "caller", text: "iyeh yiwen, activiw svp!" },
      { role: "operator", text: "d'accord a sidi." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Beni Ksila",
    id: "SYN_accident_pedestrian_001__00003",
    turns: [
      { role: "caller", text: "allo arwa7u!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda?" },
      { role: "caller", text: "beni ksila! tomobil thewwet sin arrach! ighli yiwen, idukh, wayed ithyughen adar!" },
      { role: "operator", text: "sh7al n l'blessés?" },
      { role: "caller", text: "sin! azlemd la3nayak!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Akbou, zdat la poste, en face l'école",
    id: "SYN_accident_pedestrian_002__00011",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, rani f akbou, kayen un accident. tomobil darbet un piéton." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "commune d'akbou, zdat la poste, en face l'école." },
      { role: "operator", text: "dachu yellan? est-ce qu'il est conscient?" },
      { role: "caller", text: "rah taya7 f l'erd, rah conscient chwiya, fih idamen." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Adekar, centre ville, wa7id l'jame3",
    id: "SYN_accident_pedestrian_002__00012",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo khouya, kayen wa7ed l'enfant darbouh b tomobil hna f adekar." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "commune d'adekar, centre ville, wa7id l'jame3." },
      { role: "operator", text: "ch7al n l'blessés?" },
      { role: "caller", text: "wa7ed, un petit garçon. rah yebki." },
      { role: "operator", text: "d'accord a sidi, a9lagh ntteddu-d. sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Ighram, RN26, zdat la pompe à essence",
    id: "SYN_accident_pedestrian_002__00013",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, bghit l'ambulance. kayen tomobil renverse piéton f rn26." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "f ighram, zdat la pompe à essence." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "lalla, ma rahch conscient, rah dakh." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Beni Ksila, zdat la plage, en face les pompiers 9dim",
    id: "SYN_accident_pedestrian_002__00014",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, khouya rani f beni ksila, wa7ed l'amghar darbouh, yewwet-it lbus." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "beni ksila, zdat la plage, en face les pompiers 9dim." },
      { role: "operator", text: "dachu yellan? iblessi?" },
      { role: "caller", text: "ih, rah blessé f rejlou, ma ye9derch inod." },
      { role: "operator", text: "d'accord a sidi, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amizour, cité 500 logements, bloc B, zdat l'primaire",
    id: "SYN_accident_pedestrian_002__00015",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam alaykoum. kayen accident f amizour. moto darbet mra." },
      { role: "operator", text: "anda exact? anwa l'bloc?" },
      { role: "caller", text: "f la cité 500 logements, bloc b, zdat l'primaire." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "oui, raha wa9fa mais raha t'chki men rasha." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amalou, RN12, zdat l'arret de bus",
    id: "SYN_accident_pedestrian_002__00016",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo khouya, wa7ed piéton fiyatouh f rn12." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "commune d'amalou, zdat l'arret de bus." },
      { role: "operator", text: "dachu yellan? ch7al n l'blessés?" },
      { role: "caller", text: "kayen wa7ed, un jeune. rah taya7 ou yenzel mennou ddem." },
      { role: "operator", text: "d'accord a gma, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Barbacha centre, zdat la mairie, en face l'APC",
    id: "SYN_accident_pedestrian_002__00017",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, rani f barbacha, kayen un accident de piéton, darbouh." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "barbacha centre, zdat la mairie, en face l'apc." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "ma 3labalich, rani b3id chwiya, lghachi mlammin 3lih." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance. sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Chellata, village principal, zdat sbitar sghir",
    id: "SYN_accident_pedestrian_002__00018",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, kayen un accident. tomobil darbet rajel kbir f chellata." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "commune de chellata, village principal, zdat sbitar sghir." },
      { role: "operator", text: "dachu yellan? iblessi?" },
      { role: "caller", text: "rah blessé f rasso, idamen bezzaf." },
      { role: "operator", text: "d'accord a madame, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Taourirt Ighil, la rentrée n l'village, zdat l'école primaire",
    id: "SYN_accident_pedestrian_002__00019",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, bghit n'signaler accident f taourirt ighil. un piéton darbouh." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "f la rentrée n l'village, zdat l'école primaire." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "oui, rah conscient, mais rejlou m'kessra." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Aït-Smail, RN9, zdat le barrage de police",
    id: "SYN_accident_pedestrian_002__00020",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, khouya kayen accident, renverse piéton f rn9." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "aït-smail, zdat le barrage de police." },
      { role: "operator", text: "dachu yellan? ch7al n l'blessés?" },
      { role: "caller", text: "wa7ed berk, mra, raha msat7a f l'erd, ma t'7arekch." },
      { role: "operator", text: "d'accord a sidi, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Adekar, RN12",
    id: "SYN_accident_pedestrian_003__00021",
    turns: [
      { role: "operator", text: "allo, l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam alaykoum. kayen un accident dayi, thella yiwet tomobil tewwet yiwen n piéton, darbouh." },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "g adekar, f l'embouteillage n rn12, la circulation the3mer. ighli g u-gwadroun meskin." },
      { role: "operator", text: "est-ce qu'il est conscient? dachu yellan?" },
      { role: "caller", text: "khati, idukh complètement, ul it-respirer ula mlih, balak tension tela3." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d, at-tacha l'ambulance." },
      { role: "caller", text: "sa7it khouya." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Akbou, zdat lycée",
    id: "SYN_accident_pedestrian_003__00022",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "azul. n3ayet-d f l'urgence. yiwen u-moto yewwet yiwen amghar yezger abrid. fiyatouh lhih." },
      { role: "operator", text: "anda yella dagi? wach la commune?" },
      { role: "caller", text: "g akbou, zdat lycée. l'heure agi d rush hour, bezzaf l'ghachi. amghar-agi ighli, ithyughen uqerruy-is, idamen llan." },
      { role: "operator", text: "idukh negh yaki?" },
      { role: "caller", text: "idukh chwiya, ul yezmir ula di yelhu. iban-d am tfit la crise." },
      { role: "operator", text: "d'accord, asber a sidi, aqlagh ntteddu-d tura." },
      { role: "caller", text: "sa7a, barak allahu fik." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amizour, centre ville",
    id: "SYN_accident_pedestrian_003__00023",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, ma3lich di te-activiw? yella un accident, renverse piéton. yiwen aqchich tewwet-it tomobil." },
      { role: "operator", text: "anda wani?" },
      { role: "caller", text: "amizour, g centre ville. d l'embouteillage l'weqt agi. aqchich-nni ighli, ul it-respirer ula normal, idukh meskin." },
      { role: "operator", text: "sh7al n l'blessés dagi?" },
      { role: "caller", text: "gher yiwen, aqchich-nni kan. ithyughen a t-ta3jil, ahat d crise n-wul i t-yughen mi ighli." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
      { role: "caller", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Aokas, RN9",
    id: "SYN_accident_pedestrian_003__00024",
    turns: [
      { role: "operator", text: "allo, l'7imaya l'madaniya." },
      { role: "caller", text: "salam, rani f la rn9, aokas. yella yiwen renversé piéton. yiwet tamghart teghli, tewwet-itt tomobil th-zger abrid." },
      { role: "operator", text: "dachu yellan? est-ce qu'elle est consciente?" },
      { role: "caller", text: "khati, idukh complètement. la circulation the7bes, l'ghachi bezzaf. ul t-respirer ula mlih, balak the-blessi g dhar-is." },
      { role: "operator", text: "d'accord a madame. at-tacha l'ambulance tura." },
      { role: "caller", text: "ma3lich s zerb, balak tension tela3, tban-d am tfit la crise." },
      { role: "operator", text: "aqlagh ntteddu-d, marki ghorek." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Beni Ksila, zdat l'port",
    id: "SYN_accident_pedestrian_003__00025",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo salam, yella un accident grave. yiwen fourgon yeqleb piéton, darbouh f trottoir." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "g beni ksila, zdat l'port. l'weqt n khrudj l'khedma yella l'ghachi." },
      { role: "operator", text: "sh7al n l'blessés? iblessi mlih?" },
      { role: "caller", text: "ur zrigh ara sh7al exact, llan l'ghachi bezzaf. yiwen ighli, idukh, ithyughen attas, balak llan wiyad. ul yezmir ula di yenned." },
      { role: "operator", text: "d'accord, d'accord. aqlagh ntteddu-d." },
      { role: "caller", text: "sa7it, fissa la3nayak." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Chemini, centre",
    id: "SYN_accident_pedestrian_003__00026",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, yewwet yiwen bnadm f passage clouté, fiyatouh." },
      { role: "operator", text: "anda dagi? wach la commune?" },
      { role: "caller", text: "chemini, g centre. l'embouteillage yella. ssyara tewwet-it, ighli f l'qa3a." },
      { role: "operator", text: "est-ce qu'il est conscient? iblessi?" },
      { role: "caller", text: "idukh, balak tfit la crise, ul it-respirer ula normal. ithyughen g ufus-is, idamen llan chwiya." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura s zerb." },
      { role: "caller", text: "dakur, sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Barbacha, zdat l'pompe à essence",
    id: "SYN_accident_pedestrian_003__00027",
    turns: [
      { role: "caller", text: "allo l'7imaya l'madaniya." },
      { role: "operator", text: "azul, yella accident, renverse piéton g barbacha, f la route nationale." },
      { role: "caller", text: "anda exact g barbacha?" },
      { role: "operator", text: "zdat l'pompe à essence. yiwen u-camion yewwet yiwen ameddak yezger abrid. d rush hour tura." },
      { role: "caller", text: "dachu yellan f l'blessé?" },
      { role: "operator", text: "ighli, idukh, ul it-respirer ula mlih. tban-d tfit la crise n-wul, tension tela3 ahat." },
      { role: "caller", text: "d'accord a sidi, aqlagh ntteddu-d tura." },
      { role: "operator", text: "tanmirt." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amalou, zdat l'école primaire",
    id: "SYN_accident_pedestrian_003__00028",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam 3likoum, la3nayak di te-activiw. yiwet taqchicht tewwet-itt tomobil, darbouh g amalou." },
      { role: "operator", text: "anwa l'bloc negh repère g amalou?" },
      { role: "caller", text: "zdat l'école primaire. l'weqt n khrudj l'ecole, the3mer. taqchicht-nni teghli, ithyughen bezzaf." },
      { role: "operator", text: "idukh negh yaki?" },
      { role: "caller", text: "ih idukh, tfit la crise, t-bka. ul yezmir ula di tebded." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance, asber a sidi." },
      { role: "caller", text: "sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Akfadou, RN26",
    id: "SYN_accident_pedestrian_003__00029",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, yella accident de circulation, un piéton renversé, fiyatouh." },
      { role: "operator", text: "anda wani?" },
      { role: "caller", text: "g akfadou, rn26 yella l'embouteillage. yiwet tomobil th-3fes yiwen wergaz." },
      { role: "operator", text: "dachu yellan, est-ce qu'il est conscient?" },
      { role: "caller", text: "wergaz-nni ighli, idukh chwiya. ithyughen g tharwawt-is. balak tension tela3, ul it-respirer ula normal." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
      { role: "caller", text: "sa7it, ma3lich s zerb." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Taourirt Ighil, zdat l'marché",
    id: "SYN_accident_pedestrian_003__00030",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, yella accident dayi. tomobil tewwet piéton, darbouh f trottoir." },
      { role: "operator", text: "wach la commune? anda exact?" },
      { role: "caller", text: "g taourirt ighil, zdat l'marché. d l'weqt n rush hour, the3mer l'danya." },
      { role: "operator", text: "dachu yellan? sh7al n l'blessés?" },
      { role: "caller", text: "yiwen ameddak ighli. ur zrigh ara amek yella, idukh ahat, ul yezmir ula di yelhu. ithyughen uqerruy-is." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
      { role: "caller", text: "dakur, barak allahu fik." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amizour, zdat l'hôpital",
    id: "SYN_accident_pedestrian_004__00031",
    turns: [
      { role: "caller", text: "allo l'7imaya! azlem, yiwen piéton tewwet-it ssyara dayi." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "amizour, zdat l'hôpital. yezger abrid, darbouh." },
      { role: "operator", text: "dachu yellan? est-ce qu'il est conscient?" },
      { role: "caller", text: "ih conscient, mais iblessi s udem." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
      { role: "caller", text: "sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "RN26, Akbou, en face la station",
    id: "SYN_accident_pedestrian_004__00032",
    turns: [
      { role: "caller", text: "allo les pompiers, fissa! yewwet lbus yiwen ameddak." },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. anda thellam?" },
      { role: "caller", text: "rn26, akbou, en face la station." },
      { role: "operator", text: "meskin, amek yella?" },
      { role: "caller", text: "yeghli, ul yezmir ula di inker. iblessi bezzaf!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
      { role: "caller", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Adekar, centre ville",
    id: "SYN_accident_pedestrian_004__00033",
    turns: [
      { role: "caller", text: "allo, 3ajlem svp! renverse piéton!" },
      { role: "operator", text: "m3akoum l'7imaya, anda exact?" },
      { role: "caller", text: "adekar, centre ville. taqchicht tezger passage, tewwet-itt tomobil." },
      { role: "operator", text: "est-ce qu'il y a du sang?" },
      { role: "caller", text: "khati, mais t-choqua, thebki." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
      { role: "caller", text: "barak allahu fik." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Beni Ksila, l'arrêt n l'bus",
    id: "SYN_accident_pedestrian_004__00034",
    turns: [
      { role: "caller", text: "allo l'7imaya! activiw svp, yella accident!" },
      { role: "operator", text: "dachu yellan? anda?" },
      { role: "caller", text: "beni ksila, l'arrêt n l'bus. yiwen piéton darbouh, tewwet-it moto." },
      { role: "operator", text: "ch7al n l'blessés?" },
      { role: "caller", text: "yiwen amghar. ul yettmeslay ula." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
      { role: "caller", text: "sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Chellata, zdat l'école",
    id: "SYN_accident_pedestrian_004__00035",
    turns: [
      { role: "caller", text: "allo les pompiers, 3afak azlem!" },
      { role: "operator", text: "l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "ssyara tewwet tamghart deg abrid." },
      { role: "operator", text: "anda dagi?" },
      { role: "caller", text: "chellata, zdat l'école." },
      { role: "operator", text: "iblessi?" },
      { role: "caller", text: "ul zrigh ula, teghli kan ur t-bougi ara." },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d." },
      { role: "caller", text: "sahit." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Ighram, l'entrée n village",
    id: "SYN_accident_pedestrian_004__00036",
    turns: [
      { role: "caller", text: "allo, fissa fissa! kayen accident!" },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "ighram, l'entrée n village. tomobil t-renversa piéton." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "ih, mais iblessi g uqerruy, idamen attas." },
      { role: "operator", text: "d'accord, l'ambulance di t-ru7 tura." },
      { role: "caller", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Barbacha",
    id: "SYN_accident_pedestrian_004__00037",
    turns: [
      { role: "caller", text: "allo l'7imaya! azlemd, piéton fiyatouh!" },
      { role: "operator", text: "m3akoum l'7imaya, anda wagi?" },
      { role: "caller", text: "barbacha, au niveau n trottoir, tewwet-it camionnette." },
      { role: "operator", text: "ch7al yellan?" },
      { role: "caller", text: "iwen kan, aqchich. meskin irez udhar-is." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
      { role: "caller", text: "sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Tamokra, route principale",
    id: "SYN_accident_pedestrian_004__00038",
    turns: [
      { role: "caller", text: "allo l'7imaya, s zerb svp!" },
      { role: "operator", text: "dachu yellan?" },
      { role: "caller", text: "yewwet-it lbus yiwen urgaz, yezger abrid." },
      { role: "operator", text: "wach la commune?" },
      { role: "caller", text: "tamokra, route principale." },
      { role: "operator", text: "amek yella tura?" },
      { role: "caller", text: "il est blessé au niveau n tfednin." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
      { role: "caller", text: "barak allahu fik." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Amalou, zdat l'apc",
    id: "SYN_accident_pedestrian_004__00039",
    turns: [
      { role: "caller", text: "allo, 3ajlem svp, renversé piéton!" },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "amalou, zdat l'apc. tomobil teqleb-it." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "ul zrigh ula, lghachi bezzaf dinna. ma neqder-ch nchouf." },
      { role: "operator", text: "d'accord a sidi, at-tacha l'ambulance." },
      { role: "caller", text: "sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "RN12, Adekar",
    id: "SYN_accident_pedestrian_004__00040",
    turns: [
      { role: "caller", text: "allo les pompiers! activiw!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda?" },
      { role: "caller", text: "rn12, adekar. yewwet-it camion yiwen piéton." },
      { role: "operator", text: "ch7al n l'blessés?" },
      { role: "caller", text: "iwen ameddak. yeghli, yeblessi f l'katf." },
      { role: "operator", text: "d'accord, l'ambulance tura di t-el7eq." },
      { role: "caller", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Sidi Aïch, zdat l'hôpital",
    id: "SYN_accident_pedestrian_005__00041",
    turns: [
      { role: "caller", text: "salam, tewwet yiwet tomobil yiwen weqchich dayi di sidi aïch, zdat l'hôpital. ul yezmir ula ad ihder." },
      { role: "operator", text: "l'7imaya l'madaniya n bgayet. at-defkegh numéro n l'poste n sidi aïch, marki ghorek." },
      { role: "caller", text: "an3am, efk-iyi-t-id." },
      { role: "operator", text: "d 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. dakur sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "l'Kseur, RN12",
    id: "SYN_accident_pedestrian_005__00042",
    turns: [
      { role: "caller", text: "allo, yeghli yiwen umghar deg abrid, yeqleb-it lbus dayi di l'kseur, rn12." },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya n bgayet. a sidi, at-defkegh numéro n pompiers n l'kseur, huma di qarben." },
      { role: "caller", text: "ih ma3lich." },
      { role: "operator", text: "marki: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65, sa7a gma." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Kherrata",
    id: "SYN_accident_pedestrian_005__00043",
    turns: [
      { role: "caller", text: "allo l'pompiers? yezger abrid tewwet-it tomobil dayi di kherrata, ul yeblessi ula bezaf, chwiya kan." },
      { role: "operator", text: "l'7imaya l'madaniya n bgayet f l'istima3. a madame, at-defkegh numéro n l'poste n kherrata akken di d-awden fissa." },
      { role: "caller", text: "dakur a gma, dachu-t numéro?" },
      { role: "operator", text: "034 18 51 21." },
      { role: "caller", text: "034 18 51 21. sa7it gma." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Oued Ghir, zdat l'usine",
    id: "SYN_accident_pedestrian_005__00044",
    turns: [
      { role: "caller", text: "salam alaykoum. ness3a un blessé, yiwet l'moto tewwet yiwen uqchich dagi di oued ghir zdat l'usine." },
      { role: "operator", text: "wa alaykoum salam. dagi l'7imaya n bgayet. at-defkegh numéro n oued ghir, marki ghorek: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92. dakour, ya3tik sa7a." },
      { role: "operator", text: "bla mziya." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "Chemini, la route n Sidi Aïch",
    id: "SYN_accident_pedestrian_005__00045",
    turns: [
      { role: "caller", text: "allo, yella wa yeqleb-it l'camion di chemini, f la route n sidi aïch. il est blessé." },
      { role: "operator", text: "l'7imaya l'madaniya n bgayet. at-defkegh numéro n l'poste n sidi aïch, d nutni i di d-iruhun." },
      { role: "caller", text: "iyeh, a3tih-li svp." },
      { role: "operator", text: "marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. sa7it." },
    ]
  },
  {
    type: "🚶 Accident piéton",
    incident: "accident_pedestrian",
    location: "la corniche n Aokas, RN9",
    id: "SYN_accident_pedestrian_005__00046",
    turns: [
      { role: "caller", text: "salam, kayen accident f la corniche n aokas, rn9. un piéton darbouh ssyara, yeghli." },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya n bgayet. at-defkegh numéro n l'poste n souk el tenine akken di d-awden." },
      { role: "caller", text: "ih ma3lich, efk-iyi-t-id." },
      { role: "operator", text: "d 034 09 36 13." },
      { role: "caller", text: "034 09 36 13. d'accord sa7a." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Lycée, Akbou",
    id: "SYN_accident_vehicular_001__00001",
    turns: [
      { role: "caller", text: "salam alaykoum. l'pompiers?" },
      { role: "operator", text: "an3am, m3akum l'7imaya l'madaniya. anda exact?" },
      { role: "caller", text: "g akbou, zdat lycée. collision gar tomobil d lkamyu." },
      { role: "operator", text: "ch7al n l'blessés?" },
      { role: "caller", text: "ul zrigh ula, ma nwalach." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN75, Amizour",
    id: "SYN_accident_vehicular_001__00002",
    turns: [
      { role: "caller", text: "allo, msa lkhir, l'protection civile?" },
      { role: "operator", text: "an3am. anda wagi?" },
      { role: "caller", text: "g rn75, amizour. sin yejre7 chwiya kan. tomobil tewwet g sour." },
      { role: "operator", text: "d'accord a gma, a9lagh ntteddu-d. sa7it." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Barbacha",
    id: "SYN_accident_vehicular_001__00003",
    turns: [
      { role: "caller", text: "salam. yella accident n la moto dayi g barbacha." },
      { role: "operator", text: "dachu yellan? il est conscient?" },
      { role: "caller", text: "khati, idukh meskin. ul yettwali ula. yiwen kan." },
      { role: "operator", text: "at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN24, Beni Ksila",
    id: "SYN_accident_vehicular_001__00004",
    turns: [
      { role: "caller", text: "allo salam, accident dayi g rn24 beni ksila." },
      { role: "operator", text: "an3am, is kella l'blessés?" },
      { role: "caller", text: "khati, ulach l'blessés, l'matériel kan yerrez." },
      { role: "operator", text: "d'accord, at-defkegh numéro n gendarmerie." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Chemini",
    id: "SYN_accident_vehicular_001__00005",
    turns: [
      { role: "caller", text: "allo, yella lkamyu ye9leb g abrid n chemini." },
      { role: "operator", text: "m3akum l'7imaya. est-ce que yella chkoun ye7sel?" },
      { role: "caller", text: "an3am, le chauffeur ye7sel daxel, ul yezmir ula di yeffegh." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Amalou",
    id: "SYN_accident_vehicular_001__00006",
    turns: [
      { role: "caller", text: "salam 3likoum, accident g amalou." },
      { role: "operator", text: "l'7imaya f l'istima3. dachu yellan?" },
      { role: "caller", text: "tomobil tewwet lkar." },
      { role: "operator", text: "llan l'blessés?" },
      { role: "caller", text: "ul zrigh ula tura, lghachi bezzaf." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN74, Beni Maouche",
    id: "SYN_accident_vehicular_001__00007",
    turns: [
      { role: "caller", text: "allo, l'pompiers? yella derapage dayi g rn74 zdat beni maouche." },
      { role: "operator", text: "an3am, dachu di-condition n l'blessé?" },
      { role: "caller", text: "yiwen kan, yejre7 g u9erruy, yella idamen." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance. sa7it." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Aït-R'zine",
    id: "SYN_accident_vehicular_001__00008",
    turns: [
      { role: "caller", text: "salam. yella accident g aït-r'zine." },
      { role: "operator", text: "l'7imaya l'madaniya. anda exact?" },
      { role: "caller", text: "g tournant, tomobil te9leb." },
      { role: "operator", text: "il est conscient?" },
      { role: "caller", text: "ul zrigh ula a gma, rani b3id chwiya." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN12 zdat El Kseur",
    id: "SYN_accident_vehicular_002__00009",
    turns: [
      { role: "caller", text: "allo, l'7imaya? thella tomobil teqleb deg rn12 zdat el kseur." },
      { role: "operator", text: "dayi d l'7imaya n bgayet, at-defkegh numéro n el kseur. marki ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65. d'accord, sa7it." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Chemini",
    id: "SYN_accident_vehicular_002__00010",
    turns: [
      { role: "caller", text: "salam, yella accident n la moto dagi deg chemini." },
      { role: "operator", text: "m3akoum l'7imaya n bgayet, at-defkegh numéro n sidi aïch. marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. saha khouya." },
      { role: "operator", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN9 zdat Aït-Smail",
    id: "SYN_accident_vehicular_002__00011",
    turns: [
      { role: "caller", text: "allo, kayen carambolage deg rn9 zdat aït-smail." },
      { role: "operator", text: "l'7imaya n bgayet f l'istima3, at-defkegh numéro n kherrata, marki: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21. dakur, chukran." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Aokas",
    id: "SYN_accident_vehicular_002__00012",
    turns: [
      { role: "caller", text: "azul, yella derapage n lbus dagi deg aokas." },
      { role: "operator", text: "dayi d centre n bgayet, at-defkegh numéro n souk el tenine. marki ghorek: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13. d'accord, sa7a." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN12 zdat Oued Ghir",
    id: "SYN_accident_vehicular_002__00013",
    turns: [
      { role: "caller", text: "allo, yella lkamyu yeghli deg rn12." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "zdat oued ghir." },
      { role: "operator", text: "dayi n bgayet, at-defkegh numéro n oued ghir: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92. sa7it." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Amizour",
    id: "SYN_accident_vehicular_002__00014",
    turns: [
      { role: "caller", text: "salam, thella tomobil tewwet dagi deg amizour." },
      { role: "operator", text: "l'7imaya n bgayet dayi, at-defkegh numéro n el kseur. marki ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65. aya sahit." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN26 zdat Akbou",
    id: "SYN_accident_vehicular_002__00015",
    turns: [
      { role: "caller", text: "allo, kayen accident deg rn26 zdat akbou. ul blessé ula, d la tôle kan." },
      { role: "operator", text: "dayi n bgayet, at-defkegh numéro n sidi aïch: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. dakur." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN9 Kherrata",
    id: "SYN_accident_vehicular_002__00016",
    turns: [
      { role: "caller", text: "allo l'pompiers? ssyara teqleb dagi deg rn9." },
      { role: "operator", text: "wach la commune?" },
      { role: "caller", text: "kherrata." },
      { role: "operator", text: "at-defkegh numéro n kherrata, marki ghorek: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21. sa7a." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "RN24 zdat Beni Ksila",
    id: "SYN_accident_vehicular_002__00017",
    turns: [
      { role: "caller", text: "salam alaykoum. yella accident n la moto, teqleb deg rn24 zdat beni ksila." },
      { role: "operator", text: "dayi n bgayet, at-defkegh numéro n souk el tenine: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13. sa7it." },
    ]
  },
  {
    type: "🚗 Accident véhiculaire",
    incident: "accident_vehicular",
    location: "Amalou",
    id: "SYN_accident_vehicular_002__00018",
    turns: [
      { role: "caller", text: "allo, llan snat n tonobil wwten dagi deg amalou." },
      { role: "operator", text: "l'7imaya n bgayet dayi, at-defkegh numéro n sidi aïch. marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. ya3tik sa7a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Sidi Aïch",
    id: "SYN_assault_violence_001__00026",
    turns: [
      { role: "caller", text: "allo! azlemd dagi g sidi aïch, thella ddabza! yewwet-it s lma7cha!" },
      { role: "operator", text: "l'7imaya n bgayet. cekk g sidi aïch? at-defkegh numéro n sidi aïch: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80? d'accord sa7a azlemd bark!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "El Kseur, zdat la mairie",
    id: "SYN_assault_violence_001__00027",
    turns: [
      { role: "caller", text: "allo allo! thella l'agression g el kseur zdat la mairie! yewt-it s lmus, llan idamen attas!" },
      { role: "operator", text: "m3akoum l'7imaya n bgayet. at-defkegh numéro n el kseur, marki ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65. sa7it a gma, di 3eyt-egh tura!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Kherrata",
    id: "SYN_assault_violence_001__00028",
    turns: [
      { role: "caller", text: "allo! arwa7u thella ddabza g kherrata! snat n irgazen noughen, yewwet-it s a3ekkaz!" },
      { role: "operator", text: "asber a sidi, dayi n bgayet. at-defkegh numéro n kherrata: 034 18 51 21. 3eyet ghinna!" },
      { role: "caller", text: "034 18 51 21... d'accord sa7a!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Oued Ghir",
    id: "SYN_assault_violence_001__00029",
    turns: [
      { role: "caller", text: "allo svp! amakker yekker-as i tamettut g oued ghir! yewwet-itt, theghli, tura ul tezmir ula at-nker!" },
      { role: "operator", text: "l'7imaya n bgayet. at-defkegh numéro n oued ghir, marki: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92. dakur sa7it a gma!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Adekar",
    id: "SYN_assault_violence_001__00030",
    turns: [
      { role: "caller", text: "allo azlemd! yella lmechkel g adekar! argaz yewwet gma-s s jenwa, yeblessi!" },
      { role: "operator", text: "m3akoum l'7imaya n bgayet. at-defkegh numéro n l'poste n el kseur iqerben ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65. sa7it, di s-3eyt-egh tura!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Amalou, village n Biziou",
    id: "SYN_assault_violence_001__00031",
    turns: [
      { role: "caller", text: "allo fissa! thella l'agression g amalou, village n biziou! dharbou yiwen meskin, llan idamen!" },
      { role: "operator", text: "l'7imaya n bgayet f l'istima3. at-defkegh numéro n sidi aïch, marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. d'accord sa7a!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Barbacha centre",
    id: "SYN_assault_violence_001__00032",
    turns: [
      { role: "caller", text: "allo! azlemd, thella ddabza g barbacha centre! irgazen wwten yiwen ilemzi, yett3eyit meskin!" },
      { role: "operator", text: "asber a sidi, dayi l'7imaya n bgayet. at-defkegh numéro n souk el tenine: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13? ih d'accord sa7it!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail",
    id: "SYN_assault_violence_001__00033",
    turns: [
      { role: "caller", text: "allo arwa7u! yella imenghi g aït-smail! yewt-it s ssekkin, ur yezmir ara ad i7errek!" },
      { role: "operator", text: "l'7imaya n bgayet dagi. at-defkegh numéro n kherrata: 034 18 51 21. marki-t!" },
      { role: "caller", text: "034 18 51 21. sa7it a madam!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-R'zine, l'arrêt n l'bus",
    id: "SYN_assault_violence_001__00034",
    turns: [
      { role: "caller", text: "allo svp azlemd! agression g aït-r'zine! dharbou-t g l'arrêt n l'bus, iblessi g ufus!" },
      { role: "operator", text: "m3akoum l'7imaya n bgayet. at-defkegh numéro n sidi aïch: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80. d'accord, barak allahu fik!" },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Adekar, centre ville, zdat la poste",
    id: "SYN_assault_violence_002__00035",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo salam, thella ddabza dayi, yiwen yewwet ajar-is s lmus." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "dagi di adekar, centre ville, zdat la poste, llan idamen attas." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Akfadou, village Imaghdassen, en face l'école primaire",
    id: "SYN_assault_violence_002__00036",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "azul, yella lmechkel dayi, sin irgazen noughen, yiwen yewt-it s wa3ekkaz, iblessi g uqerruy-is." },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "di commune n akfadou, village imaghdassen, en face l'école primaire." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Barbacha, cité 50 logements, bloc B, wa7id l'jame3",
    id: "SYN_assault_violence_002__00037",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, dachu yellan?" },
      { role: "caller", text: "allo, thella l'agression, krad l'3ibad wwten yiwen wergaz meskin, yeghli g lqa3a." },
      { role: "operator", text: "anda exact? anwa l'bloc?" },
      { role: "caller", text: "dagi di barbacha, cité 50 logements, bloc b, wa7id l'jame3." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "an3am, il est conscient, chwiya iblessi." },
      { role: "operator", text: "d'accord, at-defkegh numéro n la police, marki ghorek." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Amalou, route nationale RN26, zdat la pompe à essence",
    id: "SYN_assault_violence_002__00038",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam, d ttrad dayi, yella l'blessé, s zerb ma3lich." },
      { role: "operator", text: "wach la commune? anda exact?" },
      { role: "caller", text: "di amalou, route nationale rn26, zdat la pompe à essence, d l'agression wwten-t." },
      { role: "operator", text: "sh7al n l'blessés?" },
      { role: "caller", text: "yiwen, yett3eyit." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-R'zine, village Guendouz, en face l'APC",
    id: "SYN_assault_violence_002__00039",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "msa lkhir, thella ddabza meqren dayi, llan sin l'blessés, idamen g lqa3a." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "commune aït-r'zine, village guendouz, en face l'apc." },
      { role: "operator", text: "dachu yellan, wwten-ten s lmus?" },
      { role: "caller", text: "ul zrigh ula, llan idamen attas." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d la gendarmerie." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Djellil, wa7id sbitar aqdim, quartier l'moujahidine",
    id: "SYN_assault_violence_002__00040",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "allo salam, yiwen le voleur yekker-as i yiwet n tmettut, yewwet-itt." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "di beni djellil, wa7id sbitar aqdim, quartier l'moujahidine." },
      { role: "operator", text: "est-ce qu'elle est blessée?" },
      { role: "caller", text: "ih, teblessi g fusi-s, t-bki meskint." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Ksila, route nationale RN24, zdat l'plage ouest",
    id: "SYN_assault_violence_002__00041",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "sbah lkhir, yella wergaz iblessi, agression, wwten-t yagi rhun." },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "beni ksila, f la route nationale rn24, zdat l'plage ouest." },
      { role: "operator", text: "dachu s wacu yewwet-it?" },
      { role: "caller", text: "waqila s wa3ekkaz, yerrez-as adar-is." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail, cité l'indépendance, bloc 4, zdat l'école",
    id: "SYN_assault_violence_002__00042",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, svp arwa7u, thella ddabza gar ljiran, yewt-it s tesseggart!" },
      { role: "operator", text: "s tesseggart? anda exact? wach la commune?" },
      { role: "caller", text: "an3am! di aït-smail, cité l'indépendance, bloc 4, zdat l'école." },
      { role: "operator", text: "sh7al n l'blessés?" },
      { role: "caller", text: "yiwen, yeghli." },
      { role: "operator", text: "d'accord, at-defkegh numéro n la gendarmerie u aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Akfadou, centre, cité 20 logements, bloc A, deuxième étage",
    id: "SYN_assault_violence_002__00043",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam 3likoum, argaz ithedid tamettut-is s lmus, tura yewt-itt, di temmeth s idamen." },
      { role: "operator", text: "anda exact? anwa l'bloc?" },
      { role: "caller", text: "di akfadou, centre, cité 20 logements, bloc a, deuxième étage." },
      { role: "operator", text: "est-ce qu'elle est gravement blessée?" },
      { role: "caller", text: "ih, tetteffegh idamen." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance doka." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Adekar, RN12, zdat l'usine",
    id: "SYN_assault_violence_002__00044",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda?" },
      { role: "caller", text: "allo, di adekar, rn12, zdat l'usine. yella ttrad, wwten yiwen waqchich s yedghaghen." },
      { role: "operator", text: "dachu yellan? sh7al n l'blessés?" },
      { role: "caller", text: "yiwen bark, iblessi g uqerruy, il est conscient chwiya." },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d l'ambulance." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "RN12, zdat marché n Adekar",
    id: "SYN_assault_violence_003__00045",
    turns: [
      { role: "caller", text: "allo allo! l'ambulance azlemd azlemd! yaddi ya rebbi! ine9rit s lmus!" },
      { role: "operator", text: "l'7imaya l'madaniya. asber a madame s'te plaît! anda exact?" },
      { role: "caller", text: "dayi f la route rn12, zdat marché n adekar! llan idamen attas! yewwet-it s lmus! azlemd la circulation thella!" },
      { role: "operator", text: "d'accord a madame, dachu yellan? d argaz? sh7al d iblessiyen?" },
      { role: "caller", text: "iwen kan meskin! idamen! activiw s zerb!" },
      { role: "operator", text: "a9lagh ntteddu-d. at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Akfadou, zdat l'APC",
    id: "SYN_assault_violence_003__00046",
    turns: [
      { role: "caller", text: "arwa7u! azlemd! yaddi yewwet-it! yewwet-it s a3ekkaz! allo allo!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, s'il vous plaît monsieur, asber chwiya! dachu yellan?" },
      { role: "caller", text: "d amennugh dayi akfadou! d ttrad ame9ran! yewwet-it g u9erruy, yeghli! ya rebbi azlemd!" },
      { role: "operator", text: "akfadou anda exact? est-ce qu'il est conscient?" },
      { role: "caller", text: "zdat l'apc! khati, ul yezmir ula di yehder! idukh kulech! l'ambulance vite!" },
      { role: "operator", text: "d'accord a gma, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Amalou, g village",
    id: "SYN_assault_violence_003__00047",
    turns: [
      { role: "caller", text: "allo! ya rebbi! tesseggart! yudden fellas! arwa7u s zerb!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. monsieur! calmez-vous, anda?" },
      { role: "caller", text: "dayi amalou! g village! yewt-it s tesseggart, la police ula d nutni ul llin ula!" },
      { role: "operator", text: "tesseggart? sh7al n l'blessés yellan?" },
      { role: "caller", text: "iwen argaz meskin! idamen g l9a3a! azlemd azlemd!" },
      { role: "operator", text: "d'accord, marki ghorek, at-tacha l'ambulance, di n'contacti la gendarmerie." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail, en face l'école",
    id: "SYN_assault_violence_003__00048",
    turns: [
      { role: "caller", text: "allo allo! arwa7u! yaker-itt! tewwet-itt! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a madame! dachu yellan?" },
      { role: "caller", text: "iwen le voleur yewwet tamettut dayi aït-smail! yewwet-itt s lmus g webrid!" },
      { role: "operator", text: "aït-smail anda exact? est-ce que theblessi grave?" },
      { role: "caller", text: "en face l'école! ih idamen! ur tezmir ara thebded! azlemd!" },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "RN24, Beni Ksila",
    id: "SYN_assault_violence_003__00049",
    turns: [
      { role: "caller", text: "allo! agression! agression! azlemd azlemd! l'ambulance!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya. monsieur, dachu yellan? anda cekk?" },
      { role: "caller", text: "rn24, beni ksila! iwen ye7bes tomobil, yewwet ajar-iw s ssekkin! idamen!" },
      { role: "operator", text: "ssekkin? est-ce qu'il est conscient a gma?" },
      { role: "caller", text: "ul yezmir ula di yehder! yeghli g l9a3a! activiw s zerb!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance gher rn24 beni ksila tura." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Barbacha, l'arrêt n bus",
    id: "SYN_assault_violence_003__00050",
    turns: [
      { role: "caller", text: "allo l'ambulance! yaddi! lmechkel ame9ran dayi! arwa7u!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. asber a gma! anda exact?" },
      { role: "caller", text: "barbacha! l'arrêt n bus! di sin rgazen ddabza, iwen yerrez wayed s lma7cha!" },
      { role: "operator", text: "iblessi? sh7al d iblessiyen?" },
      { role: "caller", text: "iwen kan iblessi g u9erruy, idamen f l9a3a! la3nayak azlemd tura!" },
      { role: "operator", text: "d'accord a gma, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Djellil, zdat l'antenne",
    id: "SYN_assault_violence_003__00051",
    turns: [
      { role: "caller", text: "allo allo allo! la violence dayi! yewwet-it! ya rebbi azlemd!" },
      { role: "operator", text: "l'7imaya l'madaniya. madame! s'te plaît calmez-vous! anda?" },
      { role: "caller", text: "beni djellil! zdat l'antenne! yewwet-it, ur zrigh ara s wacu, balak d lmus!" },
      { role: "operator", text: "d'accord, dachu yellan i l'blessé?" },
      { role: "caller", text: "yeghli, ul yezmir ula di inudd! meskin! activiw!" },
      { role: "operator", text: "a9lagh ntteddu-d a madame." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "RN26, zdat l'usine",
    id: "SYN_assault_violence_003__00052",
    turns: [
      { role: "caller", text: "azlemd! azlemd! yewwet-it! ttrad f webrid! allo!" },
      { role: "operator", text: "l'7imaya l'madaniya, s'il vous plaît asber! anda thellam?" },
      { role: "caller", text: "rn26, zdat l'usine! iwen urgaz yekkes-d ssekkin, yewwet ameddakel-iw! idamen!" },
      { role: "operator", text: "yewwet-it s ssekkin? d'accord, cekk d ameddakel-is?" },
      { role: "caller", text: "ih ih! azlemd, l'embouteillage g webrid! activiw la3nayak!" },
      { role: "operator", text: "at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail, g village",
    id: "SYN_assault_violence_003__00053",
    turns: [
      { role: "caller", text: "ya rebbi! l'ambulance! le3yat dayi! tewwet-itt! allo!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. madame, calmez-vous! anda dagi?" },
      { role: "caller", text: "aït-smail! g village! ajiran-is tewwet-itt s a3ekkaz!" },
      { role: "operator", text: "iblessi? est-ce que d grave?" },
      { role: "caller", text: "ih g u9erruy! theghli meskint! idamen! arwa7u s zerb!" },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d, at-tacha l'ambulance." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Adekar",
    id: "SYN_assault_violence_004__00054",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, ma3lich at-defkem numéro n la police? llan ljiran ttnaghen dayi g adekar, ttrad kan, ul iblessi ula yiwen." },
      { role: "operator", text: "d'accord a sidi, d 1548. machi d l'pompiers i di t-callem." },
      { role: "caller", text: "sa7it a gma, rani ghalet." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Akfadou",
    id: "SYN_assault_violence_004__00055",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, d chchurta? kkeren-iyi téléphone-iw tura dagi g akfadou." },
      { role: "operator", text: "khati a sidi, dayi d l'pompiers. ilaq di t-ru7ed gher commissariat." },
      { role: "caller", text: "ah pardon, ul zrigh ula, rani ghalet. sa7a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Amalou",
    id: "SYN_assault_violence_004__00056",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "azul, thella ddabza n warrac dagi g amalou, tzewqen attas, d le3yat kan." },
      { role: "operator", text: "est-ce que llan idamen negh l'blessés?" },
      { role: "caller", text: "khati, ul yelli ula. d le3yat kan." },
      { role: "operator", text: "a sidi, 3ayet i la police negh la gendarmerie, machi d l'urgence nna." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-R'zine",
    id: "SYN_assault_violence_004__00057",
    turns: [
      { role: "operator", text: "allo, l'7imaya l'madaniya." },
      { role: "caller", text: "sbah lkhir. la3nayak, amek di t-3eytegh i la gendarmerie n aït-r'zine? yella yiwen ittmenacer gma." },
      { role: "operator", text: "at-defkegh numéro n ddarke, marki ghorek. 034..." },
      { role: "caller", text: "sa7it a gma, barak allahu fik." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Barbacha zdat l'busta",
    id: "SYN_assault_violence_004__00058",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo bghit ndir plainte, yewwet-iyi wa7ed g barbacha zdat l'busta." },
      { role: "operator", text: "a madame, dayi d l'pompiers. ro7i gher la police di t-depose plainte." },
      { role: "caller", text: "ah d'accord, sem7iyi rani ghalta." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Djellil",
    id: "SYN_assault_violence_004__00059",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam, thella yiwet l'bagarre g beni djellil, yerrez-as l'carreau n tomobil-is." },
      { role: "operator", text: "dachu yellan exact? yella amejru7?" },
      { role: "caller", text: "wlach, ul yeblessi ula yiwen. d l'carreau kan yerrez." },
      { role: "operator", text: "d'accord, ma ul yelli ula l'blessé, c'est la police. sa7a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "unknown",
    id: "SYN_assault_violence_004__00060",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. allo?" },
      { role: "caller", text: "[silence] awer di t-qerbed! kkes afus-ik!" },
      { role: "operator", text: "allo? a sidi? thella l'urgence?" },
      { role: "caller", text: "ah pardon! t-touchagh téléphone kan, ul yelli ula, d lmechkel kan chwiya m3a ljiran. sa7a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "RN9",
    id: "SYN_assault_violence_004__00061",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, llan sin irgazen noughen dayi g rn9, khedmen l'encombrement attas." },
      { role: "operator", text: "anwa l'blessé? thella l'urgence?" },
      { role: "caller", text: "khati, ul yewwet ula yiwen, d le3yat kan." },
      { role: "operator", text: "3ayet i la gendarmerie a sidi. sa7a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Ksila",
    id: "SYN_assault_violence_004__00062",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam 3likoum, d la police?" },
      { role: "operator", text: "khati, d l'pompiers." },
      { role: "caller", text: "ma3lich at-defked numéro n la police n beni ksila? yella l'cambriolage g l'7uma." },
      { role: "operator", text: "d'accord, marki ghorek..." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail",
    id: "SYN_assault_violence_004__00063",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "azul, yella yiwen itheded s lmus dagi g aït-smail." },
      { role: "operator", text: "est-ce que yewt-it s lmus? thella tajre7t?" },
      { role: "caller", text: "khati, ul yewwet ula, mazal." },
      { role: "operator", text: "a gma, azlem 3ayet i la gendarmerie, nekkni d l'ambulance kan." },
      { role: "caller", text: "dakur, sa7it." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Adekar centre",
    id: "SYN_assault_violence_005__00064",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "msa lkhir, tura thella ddabza dagi g adekar centre. yiwen yewt-it s lmus." },
      { role: "operator", text: "est-ce qu'il est conscient? sh7al n l'blessés?" },
      { role: "caller", text: "d yiwen kan meskin. khati, ul yezmir ula ad yehder, llan idamen attas. machi mli7 ga3." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Akfadou zdat l'apc",
    id: "SYN_assault_violence_005__00065",
    turns: [
      { role: "operator", text: "msa lkhir, m3akum l'7imaya l'madaniya." },
      { role: "caller", text: "salam, thella l'agression g akfadou, zdat l'apc. yiwen wargaz yewwet ajar-is." },
      { role: "operator", text: "dacu yellan? iblessi attas?" },
      { role: "caller", text: "ulach idamen, khati. mais yewwet-it s u3ekkaz, yeqqim g lqa3a. ul iru7 ula l sbitar." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance imir-a." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Amalou route de l'école",
    id: "SYN_assault_violence_005__00066",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, anda exact?" },
      { role: "caller", text: "sbah lkhir, llan irgazen noughen tura g amalou, route de l'école." },
      { role: "operator", text: "sh7al n l'blessés dagi?" },
      { role: "caller", text: "ur zri ara, khati ur qerbegh ara ghursen. llant tesseggart, s'il vous plaît activiw!" },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-R'zine village Guenzet",
    id: "SYN_assault_violence_005__00067",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam 3likoum, rani g aït-r'zine, village guenzet. yella yiwen yewwet tamettut, taker-as l'sac." },
      { role: "operator", text: "est-ce qu'elle est blessée?" },
      { role: "caller", text: "machi grave, th-blessi chwiya g ufus. ul thet-respirer ula mli7 s lkhel3a." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Aït-Smail centre",
    id: "SYN_assault_violence_005__00068",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, la3nayak thella l'agression dagi g aït-smail centre. yiwen ineqrit s lmus." },
      { role: "operator", text: "dachu yellan exact? iblessi?" },
      { role: "caller", text: "ih, amejru7 g uqerruy-is. ulach la police mazal, khati ur d-usan ara." },
      { role: "operator", text: "d'accord, asber a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Djellil zdat la mosquée",
    id: "SYN_assault_violence_005__00069",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, tura g beni djellil, zdat la mosquée. yella lmechkel ameqran, llan irgazen wwten wayedh." },
      { role: "operator", text: "sh7al n l'blessés? yella lmus?" },
      { role: "caller", text: "wlach lmus, khati. mais yiwen yeqqim g lqa3a, ul yettnuddum ula." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d, marki ghorek." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Beni Ksila la plage",
    id: "SYN_assault_violence_005__00070",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda exact?" },
      { role: "caller", text: "msa lkhir, dagi g beni ksila la plage. thella la violence, wa7ed yewwet ajar-is s ssekkin." },
      { role: "operator", text: "dachu yellan? iblessi attas?" },
      { role: "caller", text: "machi attas, tajre7t g ufus kan. ul yezmir ula ad yelhu, yett3eyit." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "👊 Agression/Violence",
    incident: "assault_violence",
    location: "Chemini RN26",
    id: "SYN_assault_violence_005__00071",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam 3likoum, yella yimenghi tura dagi g chemini, rn26. l'agression gar sin irgazen." },
      { role: "operator", text: "est-ce qu'il y a des blessés?" },
      { role: "caller", text: "ur zri ara, khati. ul qerbegh ula. mais wahed yett3eyit bezzaf g lqa3a." },
      { role: "operator", text: "d'accord a sidi, at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "la plage n Saket",
    id: "SYN_drowning_001__00072",
    turns: [
      { role: "caller", text: "allo l'7imaya! azlemd svp!" },
      { role: "operator", text: "l'7imaya l'madaniya, anda exact?" },
      { role: "caller", text: "la plage n saket. yiwen wqchich yeghraq g yid-a!" },
      { role: "operator", text: "teslekkem-t? il est conscient?" },
      { role: "caller", text: "an3am, maca ul it-respirer ula! 3ajlem!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
      { role: "caller", text: "sa7a." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "la plage n Aokas",
    id: "SYN_drowning_001__00073",
    turns: [
      { role: "caller", text: "allo l'7imaya fissa!" },
      { role: "operator", text: "l'7imaya f l'istima3, anda exact?" },
      { role: "caller", text: "la plage n aokas! kayen noyade!" },
      { role: "operator", text: "sh7al yellan?" },
      { role: "caller", text: "sin arrach ghreqen deg waman d yid! ul ssinen ula ad 3umen! activiw!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
      { role: "caller", text: "barak allahu fik." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "la plage n Tichy, zdat l'hotel",
    id: "SYN_drowning_002__00074",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, yella yiwen yeghra9 dayi g tichy." },
      { role: "operator", text: "anda exact g tichy? wach la commune?" },
      { role: "caller", text: "la plage n tichy, zdat l'hotel, f lill akagi khati ma yban." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Boulimat, en face l'parking",
    id: "SYN_drowning_002__00075",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, yiwen we9chich yeghli deg waman dayi g boulimat." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "boulimat, en face l'parking. ul yezmir ula ad yeffegh, d lill tura." },
      { role: "operator", text: "d'accord a sidi, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Aokas, zdat les rochers, 9bel le tunnel",
    id: "SYN_drowning_002__00076",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "msa lkhir, la3nayak d urgent, sin irgazen ghre9en g lbhar." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "g aokas, zdat les rochers, 9bel le tunnel. di mmuthen!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "le port n Saket",
    id: "SYN_drowning_002__00077",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, thella yiweth teghra9 dayi." },
      { role: "operator", text: "dachu yellan? anda?" },
      { role: "caller", text: "g le port n saket. teghli deg waman, ur thessin ara ad the3um." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Melbou, RN9, zdat la brigade n gendarmerie",
    id: "SYN_drowning_002__00078",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, kayen noyade dayi." },
      { role: "operator", text: "wach la commune? anda exact?" },
      { role: "caller", text: "g melbou, rn9, zdat la brigade n gendarmerie. yeghra9 f lill." },
      { role: "operator", text: "d'accord a sidi, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Adekar, zdat l'pont",
    id: "SYN_drowning_002__00079",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo salam, yiwen yeghra9 g asif." },
      { role: "operator", text: "anda exact a gma?" },
      { role: "caller", text: "g adekar, zdat l'pont. d lill ma yban wlac." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "ul zrigh ula." },
      { role: "operator", text: "a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tighremt, la plage, en face les bungalows",
    id: "SYN_drowning_002__00080",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "msa lkhir, yella we9chich yeghra9 dayi." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "g tighremt, la plage, en face les bungalows. nsufrith-id tura." },
      { role: "operator", text: "d'accord a sidi, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Cap Carbon, zdat l'phare",
    id: "SYN_drowning_002__00081",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, yiweth temgharth teghli deg waman." },
      { role: "operator", text: "anda exact? dachu yellan?" },
      { role: "caller", text: "g cap carbon, zdat l'phare. teghra9, d lill ur tban ara." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Les Aiguades, zdat l'parking n sidi yahia",
    id: "SYN_drowning_002__00082",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, kayen noyade dayi g l'plage." },
      { role: "operator", text: "wach la commune? anda?" },
      { role: "caller", text: "les aiguades, zdat l'parking n sidi yahia. f lill akagi khati lghachi." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Beni Ksila, zdat l'camp",
    id: "SYN_drowning_002__00083",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "azul, llan arrach ghre9en deg waman." },
      { role: "operator", text: "anda exact? ch7al n l'blessés?" },
      { role: "caller", text: "g beni ksila, zdat l'camp. llan tlatha, di ghre9en tura, d lill!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tichy",
    id: "SYN_drowning_003__00084",
    turns: [
      { role: "caller", text: "allo allo! arwa7u s zerb! aqchich yeghraq! ya rebbi! yeghraq g lbhar!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a madame! anda exact?" },
      { role: "caller", text: "g tichy! la plage tichy! ul it-respirer ula! azlemd!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d!" },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Aokas",
    id: "SYN_drowning_003__00085",
    turns: [
      { role: "caller", text: "yaddi yaddi! arwa7u azlemd! ighraq!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, chwiya s'te plaît! dachu yellan?" },
      { role: "caller", text: "g aokas! ighraq g waman! iterq-it lbhar! arwa7u!" },
      { role: "operator", text: "d'accord a sidi, aqlagh." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Cap Carbon",
    id: "SYN_drowning_003__00086",
    turns: [
      { role: "caller", text: "allo! yeghli! yeghli deg waman! ya rebbi slekk-it!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a madame! anda thella?" },
      { role: "caller", text: "g cap carbon! ighder bezzaf dayi! ul yezmir ula di ye3um!" },
      { role: "operator", text: "at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Boulimat",
    id: "SYN_drowning_003__00087",
    turns: [
      { role: "caller", text: "azlemd azlemd! yawi-t lbhar! yawi-t iker lebher! ahhhh!" },
      { role: "operator", text: "asber a madame! s'te plaît! anda amkan?" },
      { role: "caller", text: "boulimat! zdat les rochers! yeghraq meskin!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Saket",
    id: "SYN_drowning_003__00088",
    turns: [
      { role: "caller", text: "allo allo allo! la3nayak! taqchicht teghraq! fissa!" },
      { role: "operator", text: "l'7imaya l'madaniya, anda dagi? dachu yellan?" },
      { role: "caller", text: "saket! g la plage saket! teghraq ul t-respirer ula!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance!" },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Melbou",
    id: "SYN_drowning_003__00089",
    turns: [
      { role: "caller", text: "ya rebbi ya rebbi! arwa7u! sin ghreqen! ghreqen!" },
      { role: "operator", text: "asber a sidi! m3akoum l'7imaya! anda?" },
      { role: "caller", text: "melbou! g chatt n melbou! ul yezmir ula di slekk-it!" },
      { role: "operator", text: "aqlagh ntteddu-d a sidi!" },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tighremt",
    id: "SYN_drowning_003__00090",
    turns: [
      { role: "caller", text: "allo! activiw! yeghraq! yeghraq! yaddi arwa7u!" },
      { role: "operator", text: "l'7imaya l'madaniya, madame! s'te plaît! anda exact?" },
      { role: "caller", text: "tighremt! la plage tighremt! ur d-ikwal ara! vite!" },
      { role: "operator", text: "d'accord at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "RN9 Aokas",
    id: "SYN_drowning_003__00091",
    turns: [
      { role: "caller", text: "arwa7u arwa7u! yeghraq g waman!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, asber a sidi! wesh la commune?" },
      { role: "caller", text: "g aokas zdat rn9! yeghraq ul d-iban ula!" },
      { role: "operator", text: "d'accord aqlagh." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Les Aiguades",
    id: "SYN_drowning_003__00092",
    turns: [
      { role: "caller", text: "allo! la3nayak arwa7u! ighraq dayi! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya! asber s'te plaît! anda?" },
      { role: "caller", text: "les aiguades! ighraq deg waman! ul yezmir ula di ye3um!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Adekar",
    id: "SYN_drowning_003__00093",
    turns: [
      { role: "caller", text: "allo allo! fissa! yeghraq g ssedd! yaddi!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, asber a madame! anda ssedd?" },
      { role: "caller", text: "g adekar! yeghraq ul d-iban ula! azlemd!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tichy",
    id: "SYN_drowning_004__00094",
    turns: [
      { role: "caller", text: "allo l'7imaya! azlemd! yiwen weqchich yeghraq dayi g la plage n tichy!" },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "en face l'hôtel, ulach les sauveteurs!" },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "khati, nsufrith-id, ul yetneffis ula!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Boulimat",
    id: "SYN_drowning_004__00095",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "s zerb! sin warrach ghreqen dayi g boulimat!" },
      { role: "operator", text: "wach la plage?" },
      { role: "caller", text: "machi la plage surveillée, d les rochers! yiwen nsufrith-id, wayed ur yessin ara ad ye3um, mazal daxel!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d les plongeurs." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Beni Ksila",
    id: "SYN_drowning_004__00096",
    turns: [
      { role: "caller", text: "allo l'pompiers, 3ajlem! thella la noyade dayi g beni ksila." },
      { role: "operator", text: "anda exact g beni ksila?" },
      { role: "caller", text: "zdat le port. d yiwen urgaz, yeghraq, nexredj-it-id." },
      { role: "operator", text: "dachu yellan tura?" },
      { role: "caller", text: "ul yezmir ula ad yawi nnefs. khati ur d-yekwal ara." },
      { role: "operator", text: "aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Aokas",
    id: "SYN_drowning_004__00097",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo! azlemd la3nayak, taqchicht teghraq g lebhar n aokas!" },
      { role: "operator", text: "anwa l'endroit?" },
      { role: "caller", text: "zdat l'tunnel, ulach l'maître-nageur daghi!" },
      { role: "operator", text: "nsufritem-tt-id?" },
      { role: "caller", text: "khati, theghraq, ur netwala ara anda thella!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d s zerb." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Melbou",
    id: "SYN_drowning_004__00098",
    turns: [
      { role: "caller", text: "allo l'7imaya, s zerb! yiwen weqchich amectu7 yeghli deg wasif dayi g melbou!" },
      { role: "operator", text: "anda g melbou?" },
      { role: "caller", text: "zdat l'pont. nexredj-it-id yagi." },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "machi conscient, ul yet7errik ula! di yemmet!" },
      { role: "operator", text: "d'accord asber, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Saket",
    id: "SYN_drowning_004__00099",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo! t-qleb l'flouka dayi g saket, llan lghachi ghreqen!" },
      { role: "operator", text: "sh7al n lghachi?" },
      { role: "caller", text: "ur zrigh ara, ul nezmir ula a ten-n3awen, iker lebher!" },
      { role: "operator", text: "wach la plage exact?" },
      { role: "caller", text: "zdat l'port, ulach l'ambulance!" },
      { role: "operator", text: "d'accord, at-tacha les plongeurs." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Cap Carbon",
    id: "SYN_drowning_004__00100",
    turns: [
      { role: "caller", text: "allo l'pompiers! azlemd gma, yiwen urgaz yeghli deg waman g cap carbon!" },
      { role: "operator", text: "dachu yellan?" },
      { role: "caller", text: "d les rochers, yeghli, machi g la plage!" },
      { role: "operator", text: "nsufrith-id?" },
      { role: "caller", text: "khati, ur yelli ara dayi, yeghraq!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d s l'équipe de sauvetage." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Les Aiguades",
    id: "SYN_drowning_004__00101",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "3ajlem la3nayak! yiwen yeghraq dayi g les aiguades!" },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "zdat l'parking n la plage. nessuffegh-it-id tura." },
      { role: "operator", text: "amek yella?" },
      { role: "caller", text: "ul yetneffis ula, meskin! khati, ur d-yewwi ara s lexbar." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tighremt",
    id: "SYN_drowning_004__00102",
    turns: [
      { role: "caller", text: "allo l'7imaya l'madaniya! s zerb, sin warrach ghreqen g tighremt!" },
      { role: "operator", text: "anda g tighremt?" },
      { role: "caller", text: "zdat la crique. yiwen nessuffegh-it-id, wayed ulach!" },
      { role: "operator", text: "wayed mazal g waman?" },
      { role: "caller", text: "ih! wa ul yezmir ula ad yehder, yekwa." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Adekar",
    id: "SYN_drowning_004__00103",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo! yiwen uqcic yeghraq deg wasif g adekar!" },
      { role: "operator", text: "anda exact g adekar?" },
      { role: "caller", text: "machi b3id ghef centre ville. yeghli deg waman, ur d-yuli ara!" },
      { role: "operator", text: "yella daxel mazal?" },
      { role: "caller", text: "ih, ul nezmir ula a t-nessuffegh!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tichy",
    id: "SYN_drowning_005__00104",
    turns: [
      { role: "caller", text: "khouya azlem rani f la plage tichy! kayen we7ed yeghra9!" },
      { role: "operator", text: "dachu yellan?" },
      { role: "caller", text: "a9chich ghra9, ulach les sauveteurs! machi fa9t." },
      { role: "operator", text: "d'accord at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Boulimat",
    id: "SYN_drowning_005__00105",
    turns: [
      { role: "caller", text: "allo vite! 3endna noyade hna f boulimat!" },
      { role: "operator", text: "sh7al n l'blessés?" },
      { role: "caller", text: "khati ma 3labalich! ul yezmir ula ye3um, yekker lbhar! azlem!" },
      { role: "operator", text: "a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Aokas",
    id: "SYN_drowning_005__00106",
    turns: [
      { role: "caller", text: "allo l'pompiers! fissa3! zouj ghre9en f la plage aokas!" },
      { role: "operator", text: "wesh kayen? amek l'état-nsen?" },
      { role: "caller", text: "we7ed khati machi grave, lakhor ghra9 bezzaf, ul it-respirer ula!" },
      { role: "operator", text: "sa7a a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Saket",
    id: "SYN_drowning_005__00107",
    turns: [
      { role: "caller", text: "khouya l'ambulance l saket vite! kayen ta9chicht teghra9!" },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "khati, machi consciente! jebdnaha men lebhar, ulach soufl!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Melbou",
    id: "SYN_drowning_005__00108",
    turns: [
      { role: "caller", text: "allo 3ajlem! rani f melbou, we7ed l'enfant ghra9 f l'oued!" },
      { role: "operator", text: "anda exact f melbou?" },
      { role: "caller", text: "zdat ssedd! ul it-respirer ula, machi mli7 ga3!" },
      { role: "operator", text: "asber a sidi, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Beni Ksila",
    id: "SYN_drowning_005__00109",
    turns: [
      { role: "caller", text: "allo l'7imaya! bghit ambulance l beni ksila! kayen noyade!" },
      { role: "operator", text: "wesh la plage?" },
      { role: "caller", text: "ih la plage, ur zri ara sh7al! khati machi we7ed, bezzaf! azlemd!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Les Aiguades",
    id: "SYN_drowning_005__00110",
    turns: [
      { role: "caller", text: "allo l'pompiers! 3endna wa7ed ghra9 f les aiguades!" },
      { role: "operator", text: "wach il est conscient?" },
      { role: "caller", text: "ulach ga3 lwa3y! machi fa9t meskin, ul yezmir ula ad yehder!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Tighremt",
    id: "SYN_drowning_005__00111",
    turns: [
      { role: "caller", text: "khouya azlem! zouj ghre9en f la plage tighremt!" },
      { role: "operator", text: "slekkemn-ten?" },
      { role: "caller", text: "we7ed ih, lakhor khati! mazal f waman, ulach chkoun y3awen!" },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d tura." },
    ]
  },
  {
    type: "🌊 Noyade",
    incident: "drowning",
    location: "Adekar",
    id: "SYN_drowning_005__00112",
    turns: [
      { role: "caller", text: "allo vite! rani f l'oued n adekar! we7ed yeghra9!" },
      { role: "operator", text: "wesh l'état-is?" },
      { role: "caller", text: "khati machi mli7! ul yettharik ula!" },
      { role: "operator", text: "d'accord a sidi, a9lagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Adekar",
    id: "SYN_fire_building_001__00113",
    turns: [
      { role: "caller", text: "allo pompiers! azlemd, tmesst thech3el g l'batima dayi g adekar!" },
      { role: "operator", text: "dachu yellan a sidi?" },
      { role: "caller", text: "tabaqt wis tlata! yella ddaxan bezaf, l'voisin ul yezmir ula ad yerespirer!" },
      { role: "operator", text: "anwa l'bloc?" },
      { role: "caller", text: "zdat la poste! azlemd, ulach lweqt, khati machi s tagnit!" },
      { role: "operator", text: "d'accord at-tacha l'ambulance." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akfadou",
    id: "SYN_fire_building_001__00114",
    turns: [
      { role: "caller", text: "allo, 3ajlem l'pompiers, ssqef n uxxam-nnegh irgha!" },
      { role: "operator", text: "anda tzedghem exact?" },
      { role: "caller", text: "g l'village n akfadou! machi gher ddaxan, d lhib!" },
      { role: "operator", text: "est-ce que yella chkoun daxel?" },
      { role: "caller", text: "khati, neffghed merra! maca ul nexsi ula tmesst ni! activiw fissa!" },
      { role: "operator", text: "aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Barbacha",
    id: "SYN_fire_building_001__00115",
    turns: [
      { role: "caller", text: "allo l'7imaya? yella l'incendie dayi g l'restaurant!" },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "g barbacha, route principale. l'compteur iterteq, tura thech3el tmesst!" },
      { role: "operator", text: "yella chkoun daxel?" },
      { role: "caller", text: "ulach, c'est fermé la nuit. l'gardien ur yelli ara daxel." },
      { role: "operator", text: "d'accord, at-defkegh numéro n l'poste n barbacha." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amalou",
    id: "SYN_fire_building_001__00116",
    turns: [
      { role: "caller", text: "allo arwa7u s zerb! axxam n l'djar irgha dayi g amalou!" },
      { role: "operator", text: "dachu yellan?" },
      { role: "caller", text: "d l'incendie! thella yiwet n l'3ajouz daxel, ul teffugh ula!" },
      { role: "operator", text: "est-ce que theblessi?" },
      { role: "caller", text: "ul zrigh ula! machi d tmesst tamezzyant, thech3el mlih!" },
      { role: "operator", text: "d'accord a sidi aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Ksila",
    id: "SYN_fire_building_001__00117",
    turns: [
      { role: "caller", text: "allo l'pompiers! l'bouteille n l'gaz tenfejer g l'etage wis tlata!" },
      { role: "operator", text: "anda dayi?" },
      { role: "caller", text: "beni ksila, l'immeuble en face la plage! yella ddaxan bezaf!" },
      { role: "operator", text: "tzemrem at-ffughem?" },
      { role: "caller", text: "khati, ul ners ula s drouj, tmesst thekmed lescalier! 3ajlem!" },
      { role: "operator", text: "asber a madame, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aït-Smail",
    id: "SYN_fire_building_001__00118",
    turns: [
      { role: "caller", text: "allo! l'cave n l'batima nnegh thech3el!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda exact gma?" },
      { role: "caller", text: "g aït-smail, cité l'djdida. ddaxan yeffghed g l'cave!" },
      { role: "operator", text: "yella l'blessés daxel?" },
      { role: "caller", text: "ulach, maca ul nexsi ula tmesst ni. machi d lweqt n ttsen, 3ajlem!" },
      { role: "operator", text: "d'accord, marki ghorek at-tacha l'camion." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aït-R'zine",
    id: "SYN_fire_building_001__00119",
    turns: [
      { role: "caller", text: "allo, salam, 3edjled! axxam nnegh irgha!" },
      { role: "operator", text: "anda exact a madame?" },
      { role: "caller", text: "aït-r'zine, village guenzet. l'installation électrique thech3el!" },
      { role: "operator", text: "est-ce que ffughen merra l'ghachi?" },
      { role: "caller", text: "ih, maca ul nezmir ula ad nexsi l'courant! machi d l'eau i ghen-ila, 3afakoum arwa7u!" },
      { role: "operator", text: "d'accord a madame, aqlagh-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amizour",
    id: "SYN_fire_building_001__00120",
    turns: [
      { role: "caller", text: "allo l'pompiers vite! l'chenbre g l'etage wis tlata thech3el!" },
      { role: "operator", text: "wach la commune?" },
      { role: "caller", text: "amizour, l'bloc c! ddaxan bezaf g drouj!" },
      { role: "operator", text: "yella chkoun i yeblessin?" },
      { role: "caller", text: "khati, maca ul nettwali ula s ddaxan ni! ulach kifach at-ners!" },
      { role: "operator", text: "asber a sidi, l'equipe aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Chemini",
    id: "SYN_fire_building_001__00121",
    turns: [
      { role: "caller", text: "allo azlemd! timesth thech3el g wxxam g chemini!" },
      { role: "operator", text: "dachu yellan?" },
      { role: "caller", text: "l'poêle à mazout iterteq! yella ddaxan d lhib!" },
      { role: "operator", text: "kach l'blessés?" },
      { role: "caller", text: "ulach! maca ur nufi ara amek a nessexsi tmesst, ul tekhsi ula! arwa7u fissa!" },
      { role: "operator", text: "d'accord, at-tacha l'camion g chemini." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Djellil",
    id: "SYN_fire_building_001__00122",
    turns: [
      { role: "caller", text: "allo l'7imaya! yella l'incendie dayi g l'batima n l'bni!" },
      { role: "operator", text: "anda dayi?" },
      { role: "caller", text: "beni djellil, zdat l'primaire. d louh i yirghan!" },
      { role: "operator", text: "yella l'ghachi daxel?" },
      { role: "caller", text: "khati, l'chantier fergh, ul yelli ula wa7d. machi tamdakhelt, activiw qbel at-teqmed ixxamen l'djar!" },
      { role: "operator", text: "d'accord, marki ghorek l'camion aqlagh-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Adekar, centre ville, zdat la poste",
    id: "SYN_fire_building_002__00123",
    turns: [
      { role: "caller", text: "allo allo! azlemd azlemd! tech3el tmess! ya rebbi! l'batima tirgha!" },
      { role: "operator", text: "madame, l'7imaya l'madaniya f l'istima3, asber chwiya, anda exact?" },
      { role: "caller", text: "g adekar! centre ville! zdat la poste! arwa7u s zerb, yella ddaxan attas, daxel lappartement!" },
      { role: "operator", text: "dachu yellan daxel? llan lghachi?" },
      { role: "caller", text: "ih! llan drari, ul yeffugh ula yiwen! ulach l'issue de secours, aqlin hesslegh!" },
      { role: "operator", text: "d'accord a madame, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akbou, route nationale",
    id: "SYN_fire_building_002__00124",
    turns: [
      { role: "caller", text: "allo l'pompiers! azlemd! l'incendie! tech3el tmess g l'immeuble! yaddi yaddi!" },
      { role: "operator", text: "monsieur, calme-toi, m3akoum l'7imaya l'madaniya, anda dagi?" },
      { role: "caller", text: "g akbou! g la route nationale! machi l'batima n ssekna, d les locaux commerciaux! trisiti iterteq!" },
      { role: "operator", text: "est-ce que yella chkoun iblessi? qessiwen?" },
      { role: "caller", text: "khati! lghachi ffughen, mais tmess thech3el attas, ul neksi ula chwiya! d'urgence!" },
      { role: "operator", text: "d'accord agma, at-tacha les camions tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amizour, taddart n Uqemmun",
    id: "SYN_fire_building_002__00125",
    turns: [
      { role: "caller", text: "arwa7u! arwa7u! ssqef irgha! allo allo!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. a madame, s'te plaît, dachu yellan? anda?" },
      { role: "caller", text: "g amizour! taddart n uqemmun! tech3el tmess g lqermed! ya rebbi, la bouteille de gaz thella daxel!" },
      { role: "operator", text: "l'batima g daxel ur irghi ara? llan lghachi?" },
      { role: "caller", text: "ulach lghachi, ffughen yagi! mais tmess thetqerrib g lgaz! ul yezmir ula yiwen di yekcem!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d a madame, b3ed chwiya." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Ksila, zdat la plage",
    id: "SYN_fire_building_002__00126",
    turns: [
      { role: "caller", text: "allo! l'pompiers! yaddi tech3el! l'incendie! activiw!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, asber a sidi, anda exact?" },
      { role: "caller", text: "beni ksila! zdat la plage! d un bungalow de bois, irgha kamel! yella lhib attas!" },
      { role: "operator", text: "est-ce que kayen lghachi daxel?" },
      { role: "caller", text: "ur zri ara! l'porte theglaq, machi d l'maison tayemmat, d l'location! ul nesli ula i yiwen yett3eyyit!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d les camions n l'incendie." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amalou, centre, bloc B",
    id: "SYN_fire_building_002__00127",
    turns: [
      { role: "caller", text: "allo allo! 3ajlem! ddaxan yeffghed g la cave! l'batima kamel thet-respirer-ara!" },
      { role: "operator", text: "l'7imaya f l'istima3, anda exact a madame? anwa l'bloc?" },
      { role: "caller", text: "g amalou! centre! bloc b! ddaxan k7el attas!" },
      { role: "operator", text: "est-ce que yella chkoun iblessi? llan lghachi g la cave?" },
      { role: "caller", text: "khati, g la cave ulach, mais lghachi g l'étage ul yezmir ula di ffughen! lescalier yechchur d ddaxan!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d, qimet g les balcons!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aokas, en face la mairie",
    id: "SYN_fire_building_002__00128",
    turns: [
      { role: "caller", text: "ya rebbi! allo! l'pompiers! arwa7u s zerb! la cuisine tech3el!" },
      { role: "operator", text: "madame, l'7imaya f l'istima3, s'te plaît, calme-toi, anda?" },
      { role: "caller", text: "aokas! en face la mairie! takhamt n la cuisine tirgha! l'huile thech3el!" },
      { role: "operator", text: "d'accord, est-ce que tessayim at-teksim tmess?" },
      { role: "caller", text: "ul yexsi ula! ulach l'eau! machi d chwiya tmess, d l'incendie grave! rajli yettwaxneq s ddaxan!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Barbacha, l'usine n lkhechb",
    id: "SYN_fire_building_002__00129",
    turns: [
      { role: "caller", text: "allo allo! l'usine tech3el! azlemd azlemd!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda exact agma? dachu n l'usine?" },
      { role: "caller", text: "g barbacha! l'usine n lkhechb! tmesst thech3el g l'atelier!" },
      { role: "operator", text: "kayen l'ouvriers daxel? dachu yellan?" },
      { role: "caller", text: "ih! llan tlata les ouvriers daxel! ur nelli ara sure ma ffughen! l'porte theqfel, ul yeffugh ula yiwen gher tura!" },
      { role: "operator", text: "d'accord agma, aqlagh ntteddu-d avec les renforts." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Chemini, taddart n Djenane",
    id: "SYN_fire_building_002__00130",
    turns: [
      { role: "caller", text: "allo! s'il vous plaît! l'7imaya! axxam n jeddi irgha! ya yemma!" },
      { role: "operator", text: "l'7imaya f l'istima3. a madame asber, anda l'axxam-agi?" },
      { role: "caller", text: "g chemini! taddart n djenane! d axxam n lkhechb lqdim, tech3el tmess kamel!" },
      { role: "operator", text: "jeddi-m yella daxel?" },
      { role: "caller", text: "khati, jeddi yeffugh, mais l'voisin meskin yella daxel yett3eyyit! ur yezmir ara ad yeffugh! ulach amek!" },
      { role: "operator", text: "d'accord a madame, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "A t-Smail, centre ville",
    id: "SYN_fire_building_002__00131",
    turns: [
      { role: "caller", text: "allo allo! l'explosion! l'batima terteq! arwa7u fissa fissa!" },
      { role: "operator", text: "monsieur! m3akoum l'7imaya l'madaniya, dachu iterteq? anda?" },
      { role: "caller", text: "g aït-smail! centre ville! d la fuite de gaz g l'étage! tmess thech3el partout! ul yebqa ula chwiya n ssqef!" },
      { role: "operator", text: "est-ce que yella les blessés?" },
      { role: "caller", text: "ih! kayen wa7ed iblessi grave, machi chwiya! rwa7u s zerb!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d l'camion n l'incendie." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Taourirt Ighil, CEM n centre",
    id: "SYN_fire_building_002__00132",
    turns: [
      { role: "caller", text: "allo! la3nayak! l'école n drari thech3el! azlemd! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, madame, anwa l'école? anda dagi?" },
      { role: "caller", text: "g taourirt ighil! cem n centre! l'armoire électrique terteq g couloir! yella ddaxan attas!" },
      { role: "operator", text: "drari ffughen? yella chkoun iblessi?" },
      { role: "caller", text: "khati ulach l'blessés, les profs ssuffghen-ten! mais tmess thech3el, ul yexsi ula avec l'extincteur!" },
      { role: "operator", text: "d'accord a madame, at-tacha l'camion tura, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Adekar, cité des palmiers, bloc B",
    id: "SYN_fire_building_003__00133",
    turns: [
      { role: "operator", text: "allo, l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, thella tmes dagi f l'bloc." },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "adekar, cité des palmiers, bloc b." },
      { role: "operator", text: "dachu yellan dakhil, kach blessés?" },
      { role: "caller", text: "khati, ul iblessi ula yiwen, yella gher ddaxan." },
      { role: "operator", text: "d'accord, di n-tacha l'camion tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akbou, village centre, zdat l'école",
    id: "SYN_fire_building_003__00134",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "bonjour, teche3l tmes f ssqef n uxxam." },
      { role: "operator", text: "anda exact a madame? wach la commune?" },
      { role: "caller", text: "akbou, village centre, zdat l'école." },
      { role: "operator", text: "est-ce que ffughen l3ibad dakhil?" },
      { role: "caller", text: "machi lkull, thella yiwet n tmetthut ul teffugh ula dakhil." },
      { role: "operator", text: "d'accord, di n-tacha les pompiers tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amizour, Cité 200 logements, en face la poste",
    id: "SYN_fire_building_003__00135",
    turns: [
      { role: "operator", text: "allo, m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam, l'7anut n l'alimentation thech3el tmes." },
      { role: "operator", text: "wani exact f amizour?" },
      { role: "caller", text: "cité 200 logements, en face la poste." },
      { role: "operator", text: "l'bloc ur irghi ara l'fouq?" },
      { role: "caller", text: "khati, ulach l'flammes f l'étage, l'appartement ul yettwakhneq ula yiwen." },
      { role: "operator", text: "d'accord, di n-ruh tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Ksila, l'quartier n l'port, bloc 3",
    id: "SYN_fire_building_003__00136",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, dachu yellan?" },
      { role: "caller", text: "azul, thella tmes f la cave n l'batima yagi." },
      { role: "operator", text: "anda dagi?" },
      { role: "caller", text: "beni ksila, l'quartier n l'port, bloc 3." },
      { role: "operator", text: "kach l'gaz dakhil?" },
      { role: "caller", text: "khati, ul yelli ula l'gaz, ur zri ara dachu t-cause." },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Barbacha, Cité l'indépendance, zdat l'APC",
    id: "SYN_fire_building_003__00137",
    turns: [
      { role: "caller", text: "allo, l'7imaya l'madaniya." },
      { role: "operator", text: "salam, yella ddaxan yeffghed f l'appartement 3ème étage." },
      { role: "caller", text: "anda exact f barbacha?" },
      { role: "operator", text: "cité l'indépendance, dagi zdat l'apc." },
      { role: "caller", text: "est-ce que t3erddem at-sexsim tmess?" },
      { role: "operator", text: "ih, maca ul yettext7i ula, machi chwiya n tmess, d l'incendie." },
      { role: "caller", text: "d'accord, at-defkegh l'équipe di t-tacha tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aokas, route de la plage, bloc C",
    id: "SYN_fire_building_003__00138",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "sbah lkhir, thech3el tmess f l'balcon n l'étage l'fouq." },
      { role: "operator", text: "anda a madame?" },
      { role: "caller", text: "aokas, route de la plage, bloc c." },
      { role: "operator", text: "est-ce que yella wani yettwaxneq dakhil?" },
      { role: "caller", text: "khati, ulach l3ibad, l'appartement d vide, ul iblessi ula yiwen." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Chemini, centre ville, en face l'hôpital",
    id: "SYN_fire_building_003__00139",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "allo, yella ddaxan attas f les escaliers n l'bloc." },
      { role: "operator", text: "anda exact awma?" },
      { role: "caller", text: "chemini, centre ville, en face l'hôpital." },
      { role: "operator", text: "est-ce que tzemrem at-ffughem?" },
      { role: "caller", text: "khati, ur nzemmir ara, tmes thegma, ul teffugh ula yiwet n la famille l'étage 4." },
      { role: "operator", text: "d'accord, asber a sidi, aqlagh ntteddu-d s zerb." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amalou, taddart n Biziou, axxam n l'Hadj",
    id: "SYN_fire_building_003__00140",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, thech3el la bouteille n l'gaz f la cuisine." },
      { role: "operator", text: "anda exact? wach la commune?" },
      { role: "caller", text: "amalou, taddart n biziou, axxam n l'hadj." },
      { role: "operator", text: "teche3l tmess f l'appart kamel?" },
      { role: "caller", text: "machi kamel, gher la cuisine, maca ul tekhssi ula tmes." },
      { role: "operator", text: "d'accord, di n-tacha les pompiers tura, ffughet." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aït-Smail, L'quartier n l'école primaire, bloc A",
    id: "SYN_fire_building_003__00141",
    turns: [
      { role: "caller", text: "allo, l'7imaya l'madaniya." },
      { role: "operator", text: "azul, d l'compteur n trisiti i yeche3len dagi f l'batima." },
      { role: "caller", text: "anda exact f aït-smail?" },
      { role: "operator", text: "l'quartier n l'école primaire, bloc a." },
      { role: "caller", text: "kte3em le courant?" },
      { role: "operator", text: "khati, ul n-toucha ula, n-khaf, ulach tmes bzaf maca yella ddaxan." },
      { role: "caller", text: "d'accord, di n-tacha l'camion, at-defkegh numéro n sonelgaz thani." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akfadou, village Imaghdacene",
    id: "SYN_fire_building_003__00142",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam 3likoum, thech3el tmess f yiwen uxxam qdim." },
      { role: "operator", text: "anda wagi?" },
      { role: "caller", text: "akfadou, village imaghdacene." },
      { role: "operator", text: "llaan l3ibad dakhil?" },
      { role: "caller", text: "khati, d axxam abandonné, ul yezdagh ula yiwen deg-s, ur yelli ara l'gaz thani." },
      { role: "operator", text: "d'accord a sidi, di n-tacha l'camion tura." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Adekar",
    id: "SYN_fire_building_004__00143",
    turns: [
      { role: "caller", text: "allo allo! azlemd azlemd! axxam irgha dayi! yaddi ya rebbi!" },
      { role: "operator", text: "madame! s'te plait asber, anda exact?" },
      { role: "caller", text: "dayi g adekar! thech3el tmesst f l'etage! activiw!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akbou",
    id: "SYN_fire_building_004__00144",
    turns: [
      { role: "caller", text: "ya rebbi! l'appartement tech3el! arwa7u s zerb! allo allo!" },
      { role: "operator", text: "l'7imaya l'madaniya, calmi ro7em a madame, wani?" },
      { role: "caller", text: "g akbou! dagi f l'batima, yella ddaxan attas! ul nezmir ula a neffugh!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d l'pompiers." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amizour",
    id: "SYN_fire_building_004__00145",
    turns: [
      { role: "caller", text: "allo! arwa7u! tech3el l'botella n lgaz! yaddi!" },
      { role: "operator", text: "asber a sidi! anda yella l'incident?" },
      { role: "caller", text: "f amizour! dayi f l'restaurant, di iterteq! azlemd!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Aokas",
    id: "SYN_fire_building_004__00146",
    turns: [
      { role: "caller", text: "arwa7u arwa7u! ssqef irgha! ya rebbi tech3el tmes!" },
      { role: "operator", text: "l'7imaya l'madaniya, anda a madame? s'te plait asber!" },
      { role: "caller", text: "g aokas! l'bloc a, azlemd llan l'drari daxel!" },
      { role: "operator", text: "d'accord at-tacha l'pompiers!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Barbacha",
    id: "SYN_fire_building_004__00147",
    turns: [
      { role: "caller", text: "allo allo! l'cave tech3el! ddaxan yeffghed attas! azlemd!" },
      { role: "operator", text: "l'7imaya l'madaniya, calmiw ro7koum, anda dagi?" },
      { role: "caller", text: "barbacha! f l'centre, ya rebbi activiw!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Chemini",
    id: "SYN_fire_building_004__00148",
    turns: [
      { role: "caller", text: "yaddi yaddi! trisiti tech3el f l'imara! arwa7u!" },
      { role: "operator", text: "asber a gma! dachu yellan? wani?" },
      { role: "caller", text: "chemini! l'batima n l'centre, tmesst teche3l attas!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d doka." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Ksila",
    id: "SYN_fire_building_004__00149",
    turns: [
      { role: "caller", text: "allo! takhamt tirgha! arwa7u s zerb! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya, madame s'te plait asber, anda?" },
      { role: "caller", text: "beni ksila! dayi f taddart, azlemd 3afak!" },
      { role: "operator", text: "d'accord, at-tacha l'pompiers." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Akfadou",
    id: "SYN_fire_building_004__00150",
    turns: [
      { role: "caller", text: "allo allo allo! axxam yeche3l! la3nayak arwa7u!" },
      { role: "operator", text: "sidi asber! win exact?" },
      { role: "caller", text: "g akfadou! tmesst attas, ul nezmir ula a nekchem! azlemd!" },
      { role: "operator", text: "aqlagh ntteddu-d a sidi." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Taourirt Ighil",
    id: "SYN_fire_building_004__00151",
    turns: [
      { role: "caller", text: "azlemd azlemd! l'appartement tech3el! ya rebbi lhib!" },
      { role: "operator", text: "l'7imaya l'madaniya, calmi ro7em, anda dagi?" },
      { role: "caller", text: "taourirt ighil! f l'etage wis tlata, activiw!" },
      { role: "operator", text: "d'accord a madame, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amalou",
    id: "SYN_fire_building_004__00152",
    turns: [
      { role: "caller", text: "allo! drouj n l'batima che3len! arwa7u arwa7u!" },
      { role: "operator", text: "asber a sidi, s'te plait! anda exact?" },
      { role: "caller", text: "amalou! dagi nhesel f l'etage! ddaxan attas!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d s zerb." },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Cité des 500 logements, l'bloc C, troisième étage, Akbou",
    id: "SYN_fire_building_005__00153",
    turns: [
      { role: "caller", text: "allo allo allo! arwa7u azlemd! tech3el tmess! yaddi ya rebbi!" },
      { role: "operator", text: "madame! asber a madame! m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "tmess! tech3el deg lappartement! l'bloc c, dagi akbou! cité des 500 logements! arwa7u azlemd!" },
      { role: "operator", text: "asber a madame, la3nayak. anda exact deg l'bloc?" },
      { role: "caller", text: "troisième étage! yaddi, llan warrac daxel, ul zmirn ula ad ffughen! dekhan bezaf!" },
      { role: "operator", text: "d'accord a madame, aqlagh ntteddu-d tura. at-tacha l'ambulance d les pompiers." },
      { role: "caller", text: "azlemd svp! ya rebbi!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Adekar, zdat l'poste",
    id: "SYN_fire_building_005__00154",
    turns: [
      { role: "caller", text: "allo! ya rebbi! arwa7u l'pompiers! iterteq! iterteq lbotella n lgaz!" },
      { role: "operator", text: "l'7imaya l'madaniya. sidi, asber chwiya! anda iterteq?" },
      { role: "caller", text: "dagi adekar! zdat l'poste! lbatima tech3el! azlemd azlemd! lhib yeffghed g ssqef!" },
      { role: "operator", text: "d'accord, dachu yellan? est-ce qu'il y a des blessés?" },
      { role: "caller", text: "ul zrigh ula! lghachi ffughen! tmess bezaf, di yirghi lbatima kamel!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d. ttixret i tmess a sidi." },
      { role: "caller", text: "fissa 3afak! ya rebbi l'batima!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Amizour, centre ville, l'bloc n l'marché",
    id: "SYN_fire_building_005__00155",
    turns: [
      { role: "caller", text: "allo allo! l'7imaya! tmess! tmess la cave! arwa7u!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. s'te plaît a sidi, asber chwiya. anda dagi?" },
      { role: "caller", text: "amizour! centre ville g la route principale! yaddi, ddaxan yeffghed s drouj!" },
      { role: "operator", text: "wach la famille? anwa l'bloc?" },
      { role: "caller", text: "l'bloc n l'marché! ddaxan bezaf, llan lghachi hseln g l'étage! ul zmirn ula ad ffughen! azlemd, la circulation g la route!" },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d s zerb. at-defkegh l'ambulance." },
      { role: "caller", text: "fissa fissa! ya rebbi!" },
    ]
  },
  {
    type: "🏠 Incendie bâtiment",
    incident: "fire_building",
    location: "Beni Ksila, taddart, zdat l'école",
    id: "SYN_fire_building_005__00156",
    turns: [
      { role: "caller", text: "allo! azlemd azlemd! tech3el tmess dagi g uxxam! ya rebbi!" },
      { role: "operator", text: "madame! l'7imaya l'madaniya, s'te plaît asber! anda uxxam-agi?" },
      { role: "caller", text: "beni ksila! taddart, zdat l'école! trisiti iterteq, irgha uxxam!" },
      { role: "operator", text: "d'accord, asber a madame. est-ce qu'il y a des blessés?" },
      { role: "caller", text: "iyeh! yemma meskint teghli, idukh s ddaxan! ul tezmir ula ad tnudd! arwa7u 3ajlem!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura. aqlagh ntteddu-d." },
      { role: "caller", text: "azlemd svp! ddaxan bezaf!" },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Gouraya",
    id: "SYN_fire_forest_001__00057",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, rani hna f gouraya, kayen wa7ed l'feu de forêt." },
      { role: "operator", text: "dachu yellan? tmes theche3l f lghaba?" },
      { role: "caller", text: "ih, hna f les broussailles. machi kbira bezzaf, mais l'vent ydiha." },
      { role: "operator", text: "ul theqrib ula gher les maisons?" },
      { role: "caller", text: "khati, ulach les maisons tmak." },
      { role: "operator", text: "d'accord, at-tacha l'camion n les pompiers, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Adekar",
    id: "SYN_fire_forest_001__00058",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, wesh rakom? khouya bghit nsignalé kayen la3fya f lghaba ta3 adekar." },
      { role: "operator", text: "anda exact f adekar?" },
      { role: "caller", text: "f la route nationale. ddaxan bezzaf, machi sghir." },
      { role: "operator", text: "est-ce que yella danger gher taddart?" },
      { role: "caller", text: "khati, ul yezzi ula l l'7ouma, mais fissa3 di yekber." },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Tichy",
    id: "SYN_fire_forest_001__00059",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, rani f tichy, kayen wa7ed l'incendie f idurar lfouq." },
      { role: "operator", text: "dachu yellan exact? d lghaba?" },
      { role: "caller", text: "ih khouya, les arbres rhom yeche3lou. machi hda la route." },
      { role: "operator", text: "ur thewwegh ara gher l'bloc n sakanat?" },
      { role: "caller", text: "ulach sakanat, khati." },
      { role: "operator", text: "d'accord, marki ghorek, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "El Kseur",
    id: "SYN_fire_forest_001__00060",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo khouya, 3endna feu de forêt hna f el kseur, ljiha ta3 lexla." },
      { role: "operator", text: "anwa l'bloc wela anda exact?" },
      { role: "caller", text: "mor sbitar b chwiya. khati, machi qrib lih." },
      { role: "operator", text: "ul teqrib ula gher les habitations?" },
      { role: "caller", text: "ulach l'danger tura, mais bghit nkhabarkom." },
      { role: "operator", text: "sa7it, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Oued Ghir",
    id: "SYN_fire_forest_001__00061",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, kayen tmes f lghaba ta3 oued ghir, rani nchouf ddaxan yettali-d." },
      { role: "operator", text: "dachu yellan? tmes kbira?" },
      { role: "caller", text: "machi kbira bezzaf, mais l'vent raho qawi chwiya." },
      { role: "operator", text: "ul tekcem ula gher taddart?" },
      { role: "caller", text: "khati wlach. rah f lexla." },
      { role: "operator", text: "d'accord a gma, at-tacha les pompiers." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Amizour",
    id: "SYN_fire_forest_001__00062",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda?" },
      { role: "caller", text: "allo khouya, rani f amizour, kayen feu f wa7ed terrain ta3 broussaille." },
      { role: "operator", text: "dachu yellan? yella l'7achi zdat-es?" },
      { role: "caller", text: "ulach l'7achi. machi f centre ville, rah f la périphérie." },
      { role: "operator", text: "ul yewwed ula gher l'autoroute?" },
      { role: "caller", text: "khati." },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Akbou",
    id: "SYN_fire_forest_001__00063",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, 3endna incendie f lghaba hda la vallée de la soummam." },
      { role: "operator", text: "wach la commune exact?" },
      { role: "caller", text: "akbou. rani nchouf les arbres yeche3lou. machi lte7t, lfouq." },
      { role: "operator", text: "ur thettnernay ara s zerb?" },
      { role: "caller", text: "chwiya, l'essentiel ulach sakanat hda l'feu. khati." },
      { role: "operator", text: "d'accord, at-tacha l'camion." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Sidi Aich",
    id: "SYN_fire_forest_001__00064",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, wesh khouya, bghit ngoulek kayen nnare f idurar ta3 sidi aich." },
      { role: "operator", text: "anda exact? dachu yellan?" },
      { role: "caller", text: "f taghlit. khati machi f la route, ldakhel f lghaba." },
      { role: "operator", text: "ul theqrib ula gher les poteaux électriques?" },
      { role: "caller", text: "wlach, raho b3id." },
      { role: "operator", text: "sa7it, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Aokas",
    id: "SYN_fire_forest_001__00065",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, rani f aokas, kayen ddaxan kbir ta3 feu de forêt." },
      { role: "operator", text: "anda exact f aokas?" },
      { role: "caller", text: "lfouq, f la montagne. machi hda la plage, khati." },
      { role: "operator", text: "ul thewwegh ula gher l'village?" },
      { role: "caller", text: "ulach l'danger 3la l'village, mais bghit nsighnalé." },
      { role: "operator", text: "d'accord a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🌲 Feu de forêt",
    incident: "fire_forest",
    location: "Beni Ksila",
    id: "SYN_fire_forest_001__00066",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, 3endna feu hna f beni ksila, lghaba rahi teche3l." },
      { role: "operator", text: "dachu yellan? tmes f les arbres?" },
      { role: "caller", text: "ih, kayen l'vent. machi sghir, raho ykber." },
      { role: "operator", text: "ur theqrib ara gher les chalets?" },
      { role: "caller", text: "khati, ulach sakanat 9rib, mais 3ajlem." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance d les pompiers." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "autoroute n Tichy",
    id: "SYN_fire_vehicle_001__00038",
    turns: [
      { role: "caller", text: "allo allo! arwa7u azlemd! tomobil thech3el tmess dagi f l'autoroute n tichy! ya rebbi!" },
      { role: "operator", text: "madame asber chwiya! ulach l'blessés? anda exact?" },
      { role: "caller", text: "khati ulach! ul nezmir ula at-nesskhessi! arwa7u vite!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "Sidi Ahmed",
    id: "SYN_fire_vehicle_001__00039",
    turns: [
      { role: "caller", text: "yaddi yaddi! lkamyu irgha dayi g sidi ahmed! azlemd!" },
      { role: "operator", text: "asber a sidi! machi g l'pompe à essence? dachu yellan?" },
      { role: "caller", text: "khati! d l'moteur! ul ye7bes ula! tech3el tmess azlemd!" },
      { role: "operator", text: "d'accord at-tacha l'ambulance d l'camion!" },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "route n Soummam",
    id: "SYN_fire_vehicle_001__00040",
    turns: [
      { role: "caller", text: "allo! ddaxan yeffugh-d si tomobil, thech3el! azlemd g l'route n soummam!" },
      { role: "operator", text: "s'te plaît a sidi, dachu yellan? est-ce que llan l'blessés?" },
      { role: "caller", text: "ulach l'blessés machi accident! d tmess f l'moteur! 3ajlem!" },
      { role: "operator", text: "aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "Akbou",
    id: "SYN_fire_vehicle_001__00041",
    turns: [
      { role: "caller", text: "ya rebbi! ssyara teche3l dagi g akbou! di tenfejer! azlemd!" },
      { role: "operator", text: "a madame asber! chauffeur ur yeffigh ara?" },
      { role: "caller", text: "yeffegh! ulach lghachi daxel! khati! s zerb arwa7u!" },
      { role: "operator", text: "d'accord marki ghorek aqlagh-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "centre ville n Bgayet, zdat la poste",
    id: "SYN_fire_vehicle_001__00042",
    turns: [
      { role: "caller", text: "allo allo! moto teche3l tmess g centre ville n bgayet!" },
      { role: "operator", text: "d'accord, anwa l'bloc? machi zdat sbitar?" },
      { role: "caller", text: "khati! zdat la poste! ul nwala ula bab-is! azlemd!" },
      { role: "operator", text: "d'accord at-tacha l'pompiers!" },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "El Kseur",
    id: "SYN_fire_vehicle_001__00043",
    turns: [
      { role: "caller", text: "arwa7u! fourgon irgha dayi g el kseur! ya yemma!" },
      { role: "operator", text: "l'7imaya f l'istima3, asber a madame! llan l'blessés?" },
      { role: "caller", text: "ulach l'blessés kherdjen akk! ul nuki ula amek tebda! vite!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "Aokas",
    id: "SYN_fire_vehicle_001__00044",
    turns: [
      { role: "caller", text: "allo! tomobil iterteq pnew, teche3l tmess g aokas! 3ajlem!" },
      { role: "operator", text: "d'accord a sidi, machi fuite n lgaz?" },
      { role: "caller", text: "ur nezmir ara a n-approcher! l'essence yezzazel-d! ulach amdan daxel!" },
      { role: "operator", text: "d'accord l'ambulance t-rou7-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "Seddouk zdat l'jama3",
    id: "SYN_fire_vehicle_001__00045",
    turns: [
      { role: "caller", text: "azlemd azlemd! tracteur irgha g seddouk zdat l'jama3! ya rebbi!" },
      { role: "operator", text: "asber a gma! ur ye7bes ara tmes?" },
      { role: "caller", text: "khati! ul ye7bes ula! tmess t-kard attas! arwa7u vite!" },
      { role: "operator", text: "d'accord at-tacha l'camion!" },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "route n Amizour",
    id: "SYN_fire_vehicle_001__00046",
    turns: [
      { role: "caller", text: "allo! s'il vous plaît! ssyara rghid g route n amizour!" },
      { role: "operator", text: "l'7imaya l'madaniya, est-ce que d accident?" },
      { role: "caller", text: "machi accident! thech3el we7des! ulach l'blessés daxel! azlemd la3nayak!" },
      { role: "operator", text: "d'accord aqlagh ntteddu-d." },
    ]
  },
  {
    type: "🔥 Véhicule en feu",
    incident: "fire_vehicle",
    location: "Ighil Ouazzoug",
    id: "SYN_fire_vehicle_001__00047",
    turns: [
      { role: "caller", text: "allo allo! arwa7u! tomobil teche3l g ighil ouazzoug! ya yemma!" },
      { role: "operator", text: "asber a madame! ur yelli ara amdan daxel?" },
      { role: "caller", text: "khati yeffegh-d! ul inzer ula! di tenfejer arwa7u!" },
      { role: "operator", text: "d'accord at-tacha l'pompiers." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Sidi Aïch",
    id: "SYN_hazmat_001__00067",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam khouya, rani f sidi aïch, 3endna fuite nel gaz kbira f l'batiment." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n sidi aïch, marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80, saha khouya." },
      { role: "operator", text: "sa7it." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Oued Ghir",
    id: "SYN_hazmat_001__00068",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, kayen riha ta3 gaz hnaya f oued ghir." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n oued ghir, marki ghorek: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92, saha." },
      { role: "operator", text: "sa7it." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "El Kseur",
    id: "SYN_hazmat_001__00069",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam, terte9et bouteille de gaz f el kseur, l'bloc c." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n el kseur, marki ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65, ya3tik sa7a." },
      { role: "operator", text: "d'accord a sidi." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Souk El Tenine",
    id: "SYN_hazmat_001__00070",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "khouya, rani nchem riha 9awya ta3 lgaz f souk el tenine." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n souk el tenine, marki ghorek: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13, dakour." },
      { role: "operator", text: "sa7it." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Kherrata",
    id: "SYN_hazmat_001__00071",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo, kayen fuite de gaz kbira f kherrata, f la pompe." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n kherrata, marki ghorek: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21, barak allahu fik." },
      { role: "operator", text: "sa7a." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Sidi Aïch",
    id: "SYN_hazmat_001__00072",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, bghit nsignale fuite ta3 produit chimique f l'usine ta3 sidi aïch." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n sidi aïch, marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80, saha." },
      { role: "operator", text: "d'accord a sidi." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Oued Ghir",
    id: "SYN_hazmat_001__00073",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo khouya, kesserou l'tuyau ta3 lgaz f oued ghir, kayen fuite." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n oued ghir, marki ghorek: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92, sahit khouya." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "El Kseur",
    id: "SYN_hazmat_001__00074",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, kayen rri7a n lgaz 9awya f l'batiment ta3na f el kseur." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n el kseur, marki ghorek: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65, saha." },
      { role: "operator", text: "sa7it." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Souk El Tenine",
    id: "SYN_hazmat_001__00075",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "khouya, 3endna riha makhnou9a ta3 produit chimique f souk el tenine." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n souk el tenine, marki ghorek: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13." },
      { role: "operator", text: "d'accord a sidi." },
    ]
  },
  {
    type: "☣️ Matières dangereuses",
    incident: "hazmat",
    location: "Kherrata",
    id: "SYN_hazmat_001__00076",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "allo, kayen fuite lgaz goudam l'ecole f kherrata, rani khayef." },
      { role: "operator", text: "aqlagh n bgayet, at-defkegh numéro n kherrata, marki ghorek: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21, sahit." },
      { role: "operator", text: "sa7a." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Amizour",
    id: "SYN_lost_person_001__00011",
    turns: [
      { role: "caller", text: "salam alaykoum, les pompiers?" },
      { role: "operator", text: "an3am, l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "amghar yeru7 si taddart g amizour, meskin ikhouss chwiya. netnadi fellas si lmeghreb, ul t-id-nufi ula." },
      { role: "operator", text: "a sidi, la disparition d la police, marki 17." },
      { role: "caller", text: "ah dakur, di ak-fkegh numéro n la police. ya3tik sa7a." },
      { role: "operator", text: "sa7a, tsebbu 3la khir." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Gouraya",
    id: "SYN_lost_person_001__00012",
    turns: [
      { role: "caller", text: "allo, l'7imaya l'madaniya?" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "yella wa7ed u9chich yeru7 g la forêt n gouraya. netthouf fellas s les torches, tura d lill, wlach." },
      { role: "operator", text: "d'accord, dachu ism n la famille? di n-tacha l'équipe n recherche." },
      { role: "caller", text: "la famille kadi. barak allahu fik." },
      { role: "operator", text: "sa7it a gma." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Akbou",
    id: "SYN_lost_person_001__00013",
    turns: [
      { role: "caller", text: "salam, les pompiers?" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "yiweth tamghart teru7 g centre-ville n akbou. teffugh asmi yeghli yid, ul th-id-nufi ula. d amoutin meskint." },
      { role: "operator", text: "madame, pour les disparitions ru7i g la police, 17. nekkni khatina." },
      { role: "caller", text: "d'accord, di ru7egh ghli-sen tura. sa7a." },
      { role: "operator", text: "ya3tik sa7a, allah isahal." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Tichy",
    id: "SYN_lost_person_001__00014",
    turns: [
      { role: "caller", text: "sba7 lkhir, les pompiers?" },
      { role: "operator", text: "l'7imaya l'madaniya, an3am?" },
      { role: "caller", text: "ness3a a9chich yeru7 g la plage n tichy. yeffer si la3cha, mazal ul d-yughal ula." },
      { role: "operator", text: "a gma, la disparition tfat chghal n la gendarmerie 1055. marki ghorek." },
      { role: "caller", text: "ah dakur, ul zrigh ula. barak allahu fik." },
      { role: "operator", text: "sa7a a sidi." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Kherrata",
    id: "SYN_lost_person_001__00015",
    turns: [
      { role: "caller", text: "salam alaykoum." },
      { role: "operator", text: "an3am l'7imaya l'madaniya f l'istima3. anda exact?" },
      { role: "caller", text: "dagi g les gorges de kherrata, n-perdre la route. tura d lill, llan sin arrach m3aya, wlach la lumière." },
      { role: "operator", text: "d'accord, est-ce que iblessi wa7ed?" },
      { role: "caller", text: "khati, hamdullah." },
      { role: "operator", text: "a9lagh ntteddu-d, b9aw f la position." },
      { role: "caller", text: "sa7it." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Sidi Aich",
    id: "SYN_lost_person_001__00016",
    turns: [
      { role: "caller", text: "allo l'7imaya l'madaniya?" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "yeru7 u9chich n 8 ans g la cité n sidi aich. netnadi fellas, kayen d lill, ul th-nufi ula." },
      { role: "operator", text: "madame, di am-fkegh numéro n la police, marki 17. homa les recherches." },
      { role: "caller", text: "dakour, ya3tik sa7a a gma." },
      { role: "operator", text: "sa7a." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Aokas",
    id: "SYN_lost_person_001__00017",
    turns: [
      { role: "caller", text: "salam, les pompiers f l'istima3?" },
      { role: "operator", text: "an3am, l'7imaya l'madaniya." },
      { role: "caller", text: "ness3a yiweth tamghart th-disparaître g aokas zdat l'hôpital. teffugh s l9ech n sbitar, d lill tura." },
      { role: "operator", text: "a sidi, s'il vous plaît, contactez la police f 17. d la procédure n disparition." },
      { role: "caller", text: "d'accord, di th-3eyydegh tura. shukran." },
      { role: "operator", text: "sa7a." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Oued Ghir",
    id: "SYN_lost_person_001__00018",
    turns: [
      { role: "caller", text: "salam alaykoum." },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, dachu yellan?" },
      { role: "caller", text: "wa7ed amghar iru7 g la forêt n oued ghir. yeghli yid, netthouf fellas dagi, ulach. ikhouss chwiya meskin." },
      { role: "operator", text: "d'accord, di n-tacha l'équipe n recherche. anwa l'endroit exact?" },
      { role: "caller", text: "zdat la pépinière. ya3tik sa7a." },
      { role: "operator", text: "sa7it, arwa7u l la route." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "El Kseur",
    id: "SYN_lost_person_001__00019",
    turns: [
      { role: "caller", text: "allo les pompiers?" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "yeru7 yiwon u9chich g el kseur zdat la gare. yeffer si l3asser, tura yezla d lill." },
      { role: "operator", text: "a madame, l'avis de recherche d la police. 3eyyet l 17, di am-fkegh l'information." },
      { role: "caller", text: "d'accord, ul fhimgh ula. barak allahu fik." },
      { role: "operator", text: "sa7a a madame." },
    ]
  },
  {
    type: "🔍 Personne disparue",
    incident: "lost_person",
    location: "Cap Carbon",
    id: "SYN_lost_person_001__00020",
    turns: [
      { role: "caller", text: "salam alaykoum, l'7imaya l'madaniya?" },
      { role: "operator", text: "an3am f l'istima3, anda?" },
      { role: "caller", text: "a9la-gh g cap carbon, yella wa7ed l'ami i-disparaître g les pistes. tura 9rib d chtar lill, wlach réseau mli7." },
      { role: "operator", text: "est-ce que iblessi?" },
      { role: "caller", text: "ul nezmir ula at-nissin, ul th-id-nufi ula." },
      { role: "operator", text: "d'accord, a9lagh ntteddu-d s les torches." },
      { role: "caller", text: "ya3tik sa7a." },
    ]
  },
  {
    type: "🩺 Urgence médicale",
    incident: "medical_emergency",
    location: "Akfadou, zdat l'APC",
    id: "SYN_medical_emergency_001__00157",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam, ness3a yiwen urgaz dagi tfit malaise." },
      { role: "operator", text: "anda exact?" },
      { role: "caller", text: "dagi g akfadou, zdat l'apc." },
      { role: "operator", text: "wach illa conscient? dachu yellan?" },
      { role: "caller", text: "khati, idukh, ul yetnuffus ula mli7." },
      { role: "operator", text: "d'accord, at-tacha l'ambulance tura." },
      { role: "caller", text: "sa7it." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "Amizour, cite l EPLF",
    id: "SYN_natural_disaster_001__00001",
    turns: [
      { role: "caller", text: "allo, l'7imaya l'madaniya?" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. dachu yellan?" },
      { role: "caller", text: "azlemd svp! inondation daxel axxam, aman kechmend gher wekham s zerb!" },
      { role: "operator", text: "anda exact a sidi?" },
      { role: "caller", text: "dagi g amizour, cite l'eplf. ul nezmir ula di neffagh!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "route de Kherrata",
    id: "SYN_natural_disaster_001__00002",
    turns: [
      { role: "caller", text: "allo, sba7 l'khir, s'il vous plait l'pompiers!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anda exact?" },
      { role: "caller", text: "dagi route de kherrata, abrid ibele3! ghlind iblaten f la route, un grand eboulement!" },
      { role: "operator", text: "est-ce que thella des blesses?" },
      { role: "caller", text: "khati, wlach blesses, mais la circulation t7aves." },
      { role: "operator", text: "d'accord a sidi, at-tacha l'equipe." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "route n Adekar",
    id: "SYN_natural_disaster_001__00003",
    turns: [
      { role: "caller", text: "allo, 3ajlem svp! hesslen gedfel dagi!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. anda s'il vous plait?" },
      { role: "caller", text: "g route n'adekar, yella bezaf adfel. tomobilat ul zemrent ula di l7unt!" },
      { role: "operator", text: "ch7al n tomobilat i llan dinna?" },
      { role: "caller", text: "ahat khamsa, aqlagh coinces wlach amek!" },
      { role: "operator", text: "d'accord, asber a sidi, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "zdat l usine g Soummam",
    id: "SYN_natural_disaster_001__00004",
    turns: [
      { role: "caller", text: "allo, arwa7u svp, assif ihemled!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "tahemalt th-whemled wassif dagi zdat l'usine g soummam! aman di awin l'batimat!" },
      { role: "operator", text: "est-ce que thella des familles coincnees?" },
      { role: "caller", text: "waqila ih, lwa7el d waman partout!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "l ancienne ville n Bgayet, zdat la poste",
    id: "SYN_natural_disaster_001__00005",
    turns: [
      { role: "caller", text: "allo! znezla a khouya, ighli sour f chwiya n l'ghachi!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, anda exact?" },
      { role: "caller", text: "dagi g l'ancienne ville n bgayet, zdat la poste. illa un blesse meskin!" },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "ih mais irez ughil-is, azlemd!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "bloc 3 f la cite Ihaddaden",
    id: "SYN_natural_disaster_001__00006",
    turns: [
      { role: "caller", text: "allo l'pompiers! activiw svp, aman daxel l'bloc!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, anwa l'bloc?" },
      { role: "caller", text: "bloc 3 f la cite ihaddaden. tekat lehwa bezaf, le sous-sol inonde yagi!" },
      { role: "operator", text: "dachu yellan daxel? des gens?" },
      { role: "caller", text: "ulach l'ghachi, gher les compteurs d'electricite, balak di thech3el tmess!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "village n Toudja",
    id: "SYN_natural_disaster_001__00007",
    turns: [
      { role: "caller", text: "allo, la3nayak l'pompiers!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. dachu yellan?" },
      { role: "caller", text: "glissement de terrain dagi g village n toudja! abrid ittwagh completement!" },
      { role: "operator", text: "est-ce que thella tomobil i d-ighlin?" },
      { role: "caller", text: "ulach, mais abrid ibele3 3la le village. ul nezmir ula di neffagh!" },
      { role: "operator", text: "d'accord, at-defkegh numero n l'apc, marki ghorek." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "route n Tichy, zdat la plage",
    id: "SYN_natural_disaster_001__00008",
    turns: [
      { role: "caller", text: "allo, s zerb svp! ighlid wechdjra s rri7 f tomobil!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, anda exact?" },
      { role: "caller", text: "dagi g route n tichy, zdat la plage." },
      { role: "operator", text: "sh7al n l'blesses? yella l'ghachi daxel?" },
      { role: "caller", text: "ih yella le chauffeur coince daxel! azlemd, ur yezmir ara di yali!" },
      { role: "operator", text: "d'accord, aqlagh ntteddu-d yagi." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "Sidi Ahmed",
    id: "SYN_natural_disaster_001__00009",
    turns: [
      { role: "caller", text: "allo, arwa7u lwa7el yecca l'7ouma!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya. anda s'il vous plait?" },
      { role: "caller", text: "g sidi ahmed, tekat lehwa forte, lwa7el d waman daxel les maisons!" },
      { role: "operator", text: "yella chkoun iblessin?" },
      { role: "caller", text: "khati walu, mais les familles ur zemrent ara di ffghint, l'eau est tres haute!" },
      { role: "operator", text: "d'accord a madame, aqlagh ntteddu-d." },
    ]
  },
  {
    type: "⛰️ Catastrophe naturelle",
    incident: "natural_disaster",
    location: "Rue de la Liberte, Bgayet centre",
    id: "SYN_natural_disaster_001__00010",
    turns: [
      { role: "caller", text: "allo l'pompiers! ighli plafond f yiwet la femme!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3. anda exact?" },
      { role: "caller", text: "dagi f la rue de la liberte, bgayet centre. s lehwa i t-ighli!" },
      { role: "operator", text: "est-ce qu'il est conscient?" },
      { role: "caller", text: "khati, thedukh completement, idhem-itt l'plafond! 3ajlem s'il vous plait!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance imir-a." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Akfadou",
    id: "SYN_other_001__00158",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam 3likoum, ma3lich bghigh ad steqsagh f le numéro n sbitar n akfadou." },
      { role: "operator", text: "dachu yellan a sidi? d urgent?" },
      { role: "caller", text: "khati, machi urgent tura. gma ighli sbeh, idukh chwiya, awinaths sbitar. bghigh le numéro kan bach di steqsagh fellas." },
      { role: "operator", text: "d'accord, at-defkegh numéro n l'hôpital marki ghorek." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Adekar",
    id: "SYN_other_001__00159",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, allo?" },
      { role: "caller", text: "azul, bghigh ad steqsagh ma kayen numéro n l'ambulance privée dayi f adekar?" },
      { role: "operator", text: "dachu yellan? ma thella l'urgence aqlagh ntteddu-d." },
      { role: "caller", text: "khati a sidi, baba tfit la crise n-wul yagi, idukh. tura yerta7 chwiya, bghigh ad th-awiyegh l docteur privé gher l'ville." },
      { role: "operator", text: "d'accord, ul ness3a ula numéro n privé, lazem di t-steqsad f sbitar." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Amalou",
    id: "SYN_other_001__00160",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "allo le docteur? svp mmi ighli f droudj, idukh chwiya, la3nayak arwa7." },
      { role: "operator", text: "a madame, dayi d l'pompiers machi d le docteur. anda exact tura?" },
      { role: "caller", text: "ah ssuruf-iyi gheltegh f le numéro! aqlagh f amalou, machi d grave, di t-awiyegh s tomobil inu." },
      { role: "operator", text: "d'accord a madame, thella l'urgence n sbitar zdat-wem." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "A t-Smail",
    id: "SYN_other_001__00161",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "sbah lkhir, a sidi aqlagh f aït-smail, thella yiweth tafunast theghli f rrif n l'oued." },
      { role: "operator", text: "d tafunast? dachu ithyughen?" },
      { role: "caller", text: "iyeh, theghli meskint, ul thezmir ula ad t-ker, tension tela3 waqila, thehlek bezzaf." },
      { role: "operator", text: "a sidi hna n'intervenir f l3ibad. lazem di t-sawled i le vétérinaire n l'apc n aït-smail." },
      { role: "caller", text: "ah d'accord, sahit a gma." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Beni Djellil",
    id: "SYN_other_001__00162",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "salam 3likoum. bghigh lkhabar kan, sbeh thewwim yiwen wemghar ighli f marché n beni djellil, idukh..." },
      { role: "operator", text: "iyeh, n-transporti-t gher les urgences. dachu tessuther tura?" },
      { role: "caller", text: "bghigh ad steqsagh ma yella mlih? meskin yella yezdagh wehd-es." },
      { role: "operator", text: "a sidi hna ur ness3a ara les nouvelles f sbitar. sawel gher l'hôpital n beni djellil." },
      { role: "caller", text: "ya3tik sa7a, barak allahu fik." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Chemini RN74",
    id: "SYN_other_001__00163",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "salam 3likoum. bghigh ad suthregh l'intervention, theghli yiweth thejra th-meqrant f route rn74 f chemini." },
      { role: "operator", text: "theghli f l'kayas? thella l'circulation? kayen blessé?" },
      { role: "caller", text: "khati, l'circulation thekheddem, walu l3ibad. theghli f rrif, thewthi yiwen weqjun, ighli idukh meskin, ithyughen." },
      { role: "operator", text: "a sidi, l'pompiers ul n-tkharridj ula f l'qchachen d l'hwayawanat ma ul yelli ula l'danger f l'circulation." },
      { role: "caller", text: "dakour, cekk th-fehmedh, ma3lich di t-wakhregh wehdi." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Adekar",
    id: "SYN_other_002__00164",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "khouya fissa, bghit numéro ta3 l'pompiers f adekar." },
      { role: "operator", text: "dachu yellan? kayen urgence?" },
      { role: "caller", text: "khati, machi urgence. ul s3igh ula nnumro, bghit nsteqsa." },
      { role: "operator", text: "d'accord, marki ghorek." },
    ]
  },
  {
    type: "📝 Autre",
    incident: "other",
    location: "Akfadou, RN26",
    id: "SYN_other_002__00165",
    turns: [
      { role: "operator", text: "m3akoum l'7imaya l'madaniya." },
      { role: "caller", text: "wesh khouya, rani f akfadou. bghit n3ref ila rn26 mehloula?" },
      { role: "operator", text: "machi l'service nnegh. ul netdhekkel ula f les routes." },
      { role: "caller", text: "ah d'accord, ur zrigh ara. sa7it khouya." },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Sidi Aïch",
    id: "SYN_structural_collapse_001__00048",
    turns: [
      { role: "caller", text: "allo azlem, ighlid woukham fellanegh f lbatima!" },
      { role: "operator", text: "7imaya l-madaniya n bgayet. anda exact a sidi?" },
      { role: "caller", text: "dagi f sidi aïch, la dalle teghli zedaw l7ith! koulchi yeghli, yella yiwen meskin iblessi ghaf uqerruy is!" },
      { role: "operator", text: "khati a sidi, dayi n bgayet la centrale. at-defkegh numéro n l'pompiers n sidi aïch, marki ghorek: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80, d'accord, saha tura di 3eytigh fissa!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "El Kseur, zdat la poste n la ville",
    id: "SYN_structural_collapse_001__00049",
    turns: [
      { role: "caller", text: "allo l'pompiers vite! l7ith n ssiment ighli dagi f l'chantier, yella yiweth yehssel sedaw l7ith!" },
      { role: "operator", text: "7imaya l-madaniya dagi n bgayet. anda yella wagi a madame?" },
      { role: "caller", text: "atan dagi f el kseur, zdat la poste n la ville. zerb, azlemd, meskin yettwa7ebs sedaw lkherdel, ul yezmir ula di bougi!" },
      { role: "operator", text: "d'accord, dagi n bgayet la centrale. at-defkegh numéro n l'pompiers n el kseur, marki: 034 82 35 65." },
      { role: "caller", text: "034 82 35 65... sahit agma, di hawlegh tura!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Souk El Tenine, le centre ville",
    id: "SYN_structural_collapse_001__00050",
    turns: [
      { role: "caller", text: "allo 3ajlem svp, ssqef n lbrique ighli dagi, khelli lkhechba teghli ghaf yiwen!" },
      { role: "operator", text: "7imaya l-madaniya f l'istima3 n bgayet. anda wagi a sidi?" },
      { role: "caller", text: "dagi f souk el tenine, le centre ville. il est blessé, ul yezmir ula di yali, il a besoin n l'ambulance!" },
      { role: "operator", text: "d'accord, dagi n bgayet la centrale. at-defkegh numéro n l'pompiers n souk el tenine, 3ayet-asen tura: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13, aya d'accord ya3tik sa7a, c'est urgent!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Kherrata, bloc B zdat l'marché n l'khodra",
    id: "SYN_structural_collapse_001__00051",
    turns: [
      { role: "caller", text: "allo salam, fissa fissa, lbatima t-cheqeq, la dalle teghli fellanegh yagi!" },
      { role: "operator", text: "l'7imaya l'madaniya m3akoum n bgayet. anda l'bloc wagi, anda exact?" },
      { role: "caller", text: "dagi f kherrata, bloc b zdat l'marché n l'khodra. zerb ula nes3a les blessés graves, lkherdel bezzaf, ssqef ighli kamel!" },
      { role: "operator", text: "a sidi dagi n bgayet. at-defkegh numéro n l'pompiers n kherrata, marki ghorek wagi: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21, oui d'accord, saha tura di 3eytigh!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Oued Ghir, route nationale, zdat l'usine",
    id: "SYN_structural_collapse_001__00052",
    turns: [
      { role: "caller", text: "allo l'pompiers! azlemd, sour n lbiton yeghli dagi ghaf tomobil, yella amdan dakhel!" },
      { role: "operator", text: "7imaya l-madaniya n bgayet. anda yewqa3 wagi, f wani quartier?" },
      { role: "caller", text: "dagi f oued ghir, route nationale, zdat l'usine. yehssel zedaw l7it la voiture, il est bloqué, fissa azlem!" },
      { role: "operator", text: "khati sidi, dagi n bgayet. at-defkegh numéro n oued ghir, marki tura: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92... d'accord, barak allahu fik a gma." },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Sidi Aïch, l'ancienne ville",
    id: "SYN_structural_collapse_001__00053",
    turns: [
      { role: "caller", text: "allo svp, ighlid woukham lqdim, lescalier yeghli kamel, bezzaf lkherdel yella!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya n bgayet. anda exact a madame, anwa l'endroit?" },
      { role: "caller", text: "f sidi aïch, l'ancienne ville, yella yiwen amghar meskin yehssel sedaw ssiment, ul yezmir ula di ffegh!" },
      { role: "operator", text: "d'accord a madame. dagi n bgayet, at-defkegh numéro n poste n sidi aïch, marki: 034 86 07 80." },
      { role: "caller", text: "034 86 07 80, sahit a gma, di 3eytigh tura s zerb!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Souk El Tenine, l'école primaire lqdim",
    id: "SYN_structural_collapse_001__00054",
    turns: [
      { role: "caller", text: "allo salam, l7yut n l'école t-cheqeq, yiwen l7ith ighli ghaf lqermed, fissa!" },
      { role: "operator", text: "7imaya l-madaniya n bgayet. anda l'école yagi, anwa l'mkan?" },
      { role: "caller", text: "f souk el tenine, l'école primaire lqdim. t-cheqeq bezzaf, wlach les blessés ma3na l7ith yeghli, yella risque amqran!" },
      { role: "operator", text: "d'accord, a sidi n bgayet la centrale dayi. at-defkegh numéro n souk el tenine, marki: 034 09 36 13." },
      { role: "caller", text: "034 09 36 13, dakour, sahit saha, di 3eytigh tura." },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Kherrata, le centre ville",
    id: "SYN_structural_collapse_001__00055",
    turns: [
      { role: "caller", text: "allo l'pompiers, 3ajlem! la dalle n l'étage teghli ghaf les ouvriers dagi s lkherdel!" },
      { role: "operator", text: "l'7imaya l'madaniya n bgayet. anda l'étage yagi, anda exact l'chantier?" },
      { role: "caller", text: "f kherrata, le centre ville. yella sin l'ouvriers, yiwen yehssel sedaw lbiton, azlemd la3nayak il est blessé!" },
      { role: "operator", text: "d'accord, n bgayet dayi, at-defkegh numéro n poste n kherrata, marki ghorek: 034 18 51 21." },
      { role: "caller", text: "034 18 51 21, sahit, tura di 3eytigh svp!" },
    ]
  },
  {
    type: "🏗️ Effondrement",
    incident: "structural_collapse",
    location: "Oued Ghir, l'usine lqdim n ssiment",
    id: "SYN_structural_collapse_001__00056",
    turns: [
      { role: "caller", text: "allo svp, fissa fissa, yella l'effondrement f l'usine, ssiment ighli bezzaf dagi!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya n bgayet. anda l'usine a sidi, win exact?" },
      { role: "caller", text: "dagi f oued ghir, l'usine lqdim n ssiment. yella yiwen urgaz bloqué, lkhechba d lbiton teghli ghafes, azlem!" },
      { role: "operator", text: "a sidi, dagi la centrale n bgayet, at-defkegh numéro n l'pompiers n oued ghir, marki ghorek: 030 16 92 92." },
      { role: "caller", text: "030 16 92 92, d'accord ya3tik sa7a a gma!" },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Tichy",
    id: "SYN_theft_robbery_001__00021",
    turns: [
      { role: "caller", text: "allo allo! arwa7u! yaddi kcemen-d s taqqa deg yid!" },
      { role: "operator", text: "madame, asber a madame! dachu yellan?" },
      { role: "caller", text: "amakker g wexxam! yerrez tabburt! azlemd azlemd!" },
      { role: "operator", text: "anda exact a madame? at-defkegh numéro n la police, marki ghorek." },
      { role: "caller", text: "dagi g tichy! la3nayak s zerb! di yerwel!" },
      { role: "operator", text: "d'accord a madame, sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Sidi Aich",
    id: "SYN_theft_robbery_001__00022",
    turns: [
      { role: "caller", text: "allo! ya rebbi! ukren-iyi tomobil! azlemd!" },
      { role: "operator", text: "l'7imaya l'madaniya. s'te plaît a sidi, asber, dachu yellan?" },
      { role: "caller", text: "ssarraq iddem takherrust-iw dagi g sidi aich deg yid! irwel!" },
      { role: "operator", text: "a sidi, aqlagh d l'pompiers. at-defkegh numéro n la gendarmerie." },
      { role: "caller", text: "ahhhh wkeren-tt! 3ajlem! ul yezmir ula ad sberg!" },
      { role: "operator", text: "marki ghorek 1055, sa7it." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Aokas",
    id: "SYN_theft_robbery_001__00023",
    turns: [
      { role: "caller", text: "allo allo allo! wthent-iyi wkeren-iyi idrimen deg yid-agi! arwa7u!" },
      { role: "operator", text: "asber a sidi! l'7imaya f l'istima3, anda exact?" },
      { role: "caller", text: "g aokas! yaddi! amakker irwel! iblessi-yi g ufus!" },
      { role: "operator", text: "d'accord, cekk t-blessid? at-tacha l'ambulance." },
      { role: "caller", text: "iyeh! s zerb!" },
      { role: "operator", text: "aqlagh ntteddu-d, sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Akbou",
    id: "SYN_theft_robbery_001__00024",
    turns: [
      { role: "caller", text: "allo! arwa7u fissa! la3nayak!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a madame, dachu yellan?" },
      { role: "caller", text: "yella wamekker yettrez ssarure n tabburt g akbou! ya rebbi!" },
      { role: "operator", text: "a madame, ilzem la police. at-defkegh numéro-nsen, marki ghorek." },
      { role: "caller", text: "azlemd! di yekcem g llilet-agi!" },
      { role: "operator", text: "d'accord a madame, appel d'urgence, sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "El Kseur",
    id: "SYN_theft_robbery_001__00025",
    turns: [
      { role: "caller", text: "allo allo! kcemen l'hanout! arwa7u fissa!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a sidi, dachu yellan?" },
      { role: "caller", text: "amakker g l'hanout-iw g el kseur! yerrez tabburt deg yid!" },
      { role: "operator", text: "a sidi, ilzem la police. at-defkegh numéro n la police." },
      { role: "caller", text: "ya rebbi iddem kulesh! azlemd!" },
      { role: "operator", text: "marki ghorek 1548, sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Amizour",
    id: "SYN_theft_robbery_001__00026",
    turns: [
      { role: "caller", text: "allo allo allo! arwa7u! kcemen-d axxam!" },
      { role: "operator", text: "asber a madame! anda exact?" },
      { role: "caller", text: "g amizour! wthent gma deg yid, iblessi attas g uqerruy! amakker irwel!" },
      { role: "operator", text: "d'accord, est-ce qu'il est conscient? sh7al n l'blessés?" },
      { role: "caller", text: "yiwen! meskin! azlemd azlemd! yaddi!" },
      { role: "operator", text: "at-tacha l'ambulance d la police, aqlagh ntteddu-d. sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Tazmalt",
    id: "SYN_theft_robbery_001__00027",
    turns: [
      { role: "caller", text: "allo! ya rebbi! wkeren la7liy-iw! arwa7u!" },
      { role: "operator", text: "l'7imaya l'madaniya, madame s'te plaît asber! anda?" },
      { role: "caller", text: "g tazmalt! amakker irwel s ddheb g llilet! azlemd!" },
      { role: "operator", text: "a madame, l'pompiers dayi. at-defkegh numéro n la gendarmerie." },
      { role: "caller", text: "ahhhh s zerb! di yerwel s wakk!" },
      { role: "operator", text: "d'accord, marki ghorek, sa7it." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Oued Ghir",
    id: "SYN_theft_robbery_001__00028",
    turns: [
      { role: "caller", text: "allo allo! yaddi llan imakkaren g l'bloc!" },
      { role: "operator", text: "asber a sidi, l'7imaya f l'istima3. anda l'bloc?" },
      { role: "caller", text: "dagi g oued ghir! yerrez lqfel n tabburt deg yid! arwa7u!" },
      { role: "operator", text: "a sidi, at-defkegh numéro n la police, maci l'ambulance." },
      { role: "caller", text: "activiw la3nayak! ul yezmir ula ad rregh lbal!" },
      { role: "operator", text: "d'accord a sidi, sa7a." },
    ]
  },
  {
    type: "🚨 Vol/Cambriolage",
    incident: "theft_robbery",
    location: "Bejaia centre",
    id: "SYN_theft_robbery_001__00029",
    turns: [
      { role: "caller", text: "allo allo! arwa7u! yaddi! ssarraq!" },
      { role: "operator", text: "l'7imaya l'madaniya, asber a sidi! dachu yellan?" },
      { role: "caller", text: "dharbou gma g bejaia centre deg yid! wkeren-as idrimen! iblessi!" },
      { role: "operator", text: "sh7al n l'blessés? est-ce qu'il est conscient?" },
      { role: "caller", text: "ih! meskin! azlemd azlemd! ahhhh!" },
      { role: "operator", text: "d'accord, at-tacha l'ambulance. aqlagh ntteddu-d. sa7it." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "RN9, Aokas",
    id: "SYN_accident_vehicular_003__00019",
    turns: [
      { role: "caller", text: "allo, l'7imaya l'madaniya?" },
      { role: "operator", text: "oui, l'7imaya l'madaniya f l'istima3. dachu yellan?" },
      { role: "caller", text: "s'il vous plaît, bghit saqsi, est-ce que abrid n rn9 g aokas yebla3? nnan-d thella accident, rani mze3fan, di ru7egh s zerb!" },
      { role: "operator", text: "madame, dagi d les urgences, ul nesa ula les informations g l'état n la route. marki numéro n la gendarmerie." },
      { role: "caller", text: "ah dakour, ma3lich, sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "RN12, Adekar",
    id: "SYN_accident_vehicular_003__00020",
    turns: [
      { role: "caller", text: "allo, khouya l'mécanicien?" },
      { role: "operator", text: "khati a gma, m3akoum l'7imaya l'madaniya n bejaia." },
      { role: "caller", text: "ah ya rebbi! rani ghalet f l'numéro. tomobil inu te7bes dagi g rn12 zdat adekar, bghit l'dépannage, activiw!" },
      { role: "operator", text: "a monsieur, dagi d les pompiers, machi dépannage. at-defkegh numéro n la police balak di 3awnen cekk." },
      { role: "caller", text: "khati khati, rani ghalet, sa7it." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "cité des palmiers, Akbou",
    id: "SYN_accident_vehicular_003__00021",
    turns: [
      { role: "caller", text: "allo les pompiers? azlem azlem!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3, anda exact? dachu yellan?" },
      { role: "caller", text: "dagi g akbou, cité des palmiers! yella yiwen wemchich meskin ye7sel g ttejra, ul yezmir ula di yeghli!" },
      { role: "operator", text: "a madame, nbeddel les urgences graves qbel. asber chwiya, ma yella l'équipe disponible di n-tacha l'camion." },
      { role: "caller", text: "d'accord, ma3lich, sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "centre ville, Amizour",
    id: "SYN_accident_vehicular_003__00022",
    turns: [
      { role: "caller", text: "allo l'7imaya! arwa7u tura!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "dagi g amizour, centre ville. llan des jeunes qqelben s les motos, diran le bruit bezzaf, ul nezmir ula a nets!" },
      { role: "operator", text: "a sidi, machi d l'7imaya l'madaniya i di t-regliya annect-a. appeler la police, numérou nsen d 17." },
      { role: "caller", text: "ah d'accord, rani ghalet, ya3tik sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Barbacha",
    id: "SYN_accident_vehicular_003__00023",
    turns: [
      { role: "caller", text: "allo, la sonelgaz?" },
      { role: "operator", text: "khati a madame, l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "oh pardon, rani ghalet. bghit nqelleb 3lach ulach trisiti dagi g barbacha. diran l'coupure yagi sa3tin, rani mazrub bghit ntayeb!" },
      { role: "operator", text: "madame, dagi d les pompiers. 3eyet i sonelgaz. at-defkegh numéro nsen marki ghorek." },
      { role: "caller", text: "khati c'est bon, sa7it a gma." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Chemini",
    id: "SYN_accident_vehicular_003__00024",
    turns: [
      { role: "operator", text: "allo, l'7imaya l'madaniya f l'istima3?" },
      { role: "caller", text: "... (bruit de moteur) ... azlem a khouya, accélérer chwiya, di n-rate l'rendez-vous g chemini!" },
      { role: "operator", text: "allo? est-ce que tesli-d? m3akoum l'pompiers!" },
      { role: "caller", text: "... (voix lointaine) ... attention au virage! ..." },
      { role: "operator", text: "allo? d'accord, d l'appel par erreur, rani n-coupi." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "la plage, Beni Ksila",
    id: "SYN_accident_vehicular_003__00025",
    turns: [
      { role: "caller", text: "allo l'pompiers?" },
      { role: "operator", text: "oui, l'7imaya l'madaniya f l'istima3, anda exact?" },
      { role: "caller", text: "rani g la plage n beni ksila, ssyara inu te7sel g rmel. ul nezmir ula di n-teffegh! actiview awid l'camion!" },
      { role: "operator", text: "a sidi, ur n-tacha ara l'ambulance ou l'camion i ssyara te7sel, machi d urgence. chercher un tracteur wela dépannage g l'coin." },
      { role: "caller", text: "ah d'accord, sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Tichy",
    id: "SYN_drowning_001__00030",
    turns: [
      { role: "caller", text: "allo allo! azlemd azlemd! aqchich yeghraq deg lebhar! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya. asber a madame, anda exact?" },
      { role: "caller", text: "tichy! la plage! ah... asber... khati khati, yeffegh-d, c'est bon. ul yeblessi ula." },
      { role: "operator", text: "yeffegh-d? d'accord a madame, thekhle3d-agh ssker." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "unknown",
    id: "SYN_drowning_001__00031",
    turns: [
      { role: "caller", text: "ya rebbi! arwa7u! yeghraq wuxxam! aman bezaf!" },
      { role: "operator", text: "l'7imaya l'madaniya. dachu yellan? yeghraq umdan?" },
      { role: "caller", text: "khati! la fuite d'eau f l'batima! aman di yawi kolchi! t-tuyau iterteq!" },
      { role: "operator", text: "madame, machi d l'pompiers i l'fuite. at-defkegh numéro n l'ade." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "unknown",
    id: "SYN_drowning_001__00032",
    turns: [
      { role: "caller", text: "allo allo fissa! yeghraq sbitar! azlemd a khouya l'plombier!" },
      { role: "operator", text: "m3akoum l'7imaya l'madaniya. dachu l'plombier?" },
      { role: "caller", text: "ah... machi l'plombier? rani ghalet f numéro, samhi a gma!" },
      { role: "operator", text: "d'accord, coupigh." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Souk El Tenine",
    id: "SYN_drowning_001__00033",
    turns: [
      { role: "caller", text: "azlemd azlemd svp! yeghraq meskin! ya rebbi yetteghriq!" },
      { role: "operator", text: "l'7imaya l'madaniya. asber a sidi, anwa ighraqen? anda?" },
      { role: "caller", text: "l'kelb inu! g asif n souk el tenine! ur yessin ara ad ye3um!" },
      { role: "operator", text: "sidi, ul ntteddu ula i l'kelb, c'est pas une urgence vitale." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Saket",
    id: "SYN_drowning_001__00034",
    turns: [
      { role: "caller", text: "allo allo! arwa7u! aman bezaf! tomobil inu teghraq!" },
      { role: "operator", text: "l'7imaya l'madaniya. asber a sidi, thella la victime?" },
      { role: "caller", text: "khati khati, ulach l'blessés. gher tomobil tebloka g waman f la route n saket." },
      { role: "operator", text: "ma ulach l'blessés, 3ayet i l'dépannage. sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "unknown",
    id: "SYN_drowning_001__00035",
    turns: [
      { role: "caller", text: "allo svp! yeghli! yeghraq f la piscine! ya rebbi!" },
      { role: "operator", text: "l'7imaya l'madaniya! chkoun yeghraqen? aqchich?" },
      { role: "caller", text: "khati! le ballon inu! yeghraq g waman!" },
      { role: "operator", text: "a taqchicht, machi d l'pompiers i le ballon. raccrochi." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Aokas",
    id: "SYN_drowning_001__00036",
    turns: [
      { role: "caller", text: "ya rebbi arwa7u! gma yeghraq g lwa7ed! azlemd!" },
      { role: "operator", text: "l'7imaya l'madaniya. anda exact lwa7ed agi?" },
      { role: "caller", text: "g aokas... asber... ah le hmar, it-jouer-ara kan! il fait semblant! samhi a sidi." },
      { role: "operator", text: "d'accord, thekhle3d-agh f batel. sa7a." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "unknown",
    id: "SYN_drowning_001__00037",
    turns: [
      { role: "caller", text: "allo allo! l'urgence! aman ulach! wlach aman g l'batima!" },
      { role: "operator", text: "l'7imaya l'madaniya. d'accord, mais dachu yellan? thech3el tmess?" },
      { role: "caller", text: "khati! coupand aman yagi 3 jours! rani mrid!" },
      { role: "operator", text: "a sidi, machi d l'pompiers. 3ayet i l'algérienne des eaux. sa7it." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Adekar, RN12",
    id: "SYN_accident_pedestrian_001__00004",
    turns: [
      { role: "caller", text: "allo l'7imaya!" },
      { role: "operator", text: "oui l'7imaya l'madaniya tfadel." },
      { role: "caller", text: "khouya wesh bikoum majitouch, kayen circulation kbira hna f rn12 jihet adekar, kayen wahed l'piéton bgha yeqta3 l'autoroute, w wahed b l'oto freina sec. ma darbouh ma walou, kayen ghir l'haws w l'guelba, le piéton rahou ydabz m3a chouffour." },
      { role: "operator", text: "ya khouya dachu yellan? kayen des blessés?" },
      { role: "caller", text: "non ul yelli ula blessé, walou, machi accident, bghit bark tgoulou l la gendarmerie yjiw ysagmu l'abrid." },
      { role: "operator", text: "3ayet l la gendarmerie khouya, hna ul ndakhel ula." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Beni Ksila",
    id: "SYN_accident_pedestrian_001__00005",
    turns: [
      { role: "caller", text: "allo khouya!" },
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "khouya rani f beni ksila, wesh dirtouna b had les ralentisseurs, chaque fois les voitures yfreiniw ydirou l'bruit, w les piétons yqet3ou f n'importe quel blasa, rani nbat ma nergoudch, bghit nchki." },
      { role: "operator", text: "ya sidi, hna l'7imaya l'madaniya, machi la mairie, rak ghalet f l'appel." },
      { role: "caller", text: "kifach machi ntouma li tdirou les plaques ta3 les piétons?" },
      { role: "operator", text: "khati a sidi, 3ayet l l'apc, bonne journée." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Barbacha",
    id: "SYN_accident_pedestrian_001__00006",
    turns: [
      { role: "caller", text: "allo!" },
      { role: "operator", text: "oui l'7imaya l'madaniya, dachu yellan?" },
      { role: "caller", text: "khouya wesh kayen f barbacha? rani nchouf l'ambulance ta3koum daret sirène w ray7a zerb, wesh kayen accident piéton wela wesh sra?" },
      { role: "operator", text: "ya khouya ul nmed ula les informations f téléphone, c'est confidentiel, 3leh rak tseqsi?" },
      { role: "caller", text: "non ghir bghit na3ref, chkoun darbouh, balak wahed men l'famille ta3na." },
      { role: "operator", text: "si kayen haja y3aytoulek, ma tchedlnech l'ligne s'il vous plaît pour rien." },
      { role: "caller", text: "d'accord semehli khouya." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Chemini",
    id: "SYN_accident_pedestrian_001__00007",
    turns: [
      { role: "caller", text: "allo l'pompiers!" },
      { role: "operator", text: "oui l'7imaya." },
      { role: "caller", text: "khouya rani hna f chemini, l'arrêt ta3 l'bus, wahed l'camion kan rayah ydir accident grave, faillit yrenverser wahed l'piéton, un petit garçon, meskin c'était juste!" },
      { role: "operator", text: "d'accord, est-ce que darbouh? kayen blessé?" },
      { role: "caller", text: "non khati, l'enfant hrab, ma darbouhch, w l'camion kml triqou. bghit nsignaler bark beli kayen danger f had l'virage." },
      { role: "operator", text: "ya khouya hmdlh li ma sra walou, mais hna njiw ki ykoun accident, 3ayet l la commune ydirou ralentisseur." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Taourirt Ighil",
    id: "SYN_accident_pedestrian_001__00008",
    turns: [
      { role: "caller", text: "allo l'7imaya." },
      { role: "operator", text: "l'7imaya f l'istima3." },
      { role: "caller", text: "khouya rani n3ayetlek 3la l'accident piéton li sra sba7 f taourirt ighil, win darbouh wahed b l'moto." },
      { role: "operator", text: "oui, dachu tebghid?" },
      { role: "caller", text: "bghit na3ref win ditouh, l sbitar ta3 akbou wela l sbitar ta3 bejaia? rani l'cousin ta3ou w ma 3reftch win nrouh." },
      { role: "operator", text: "at-defkegh l'information, d'accord? ditnah l urgences n akbou, rahou tema." },
      { role: "caller", text: "ya3tik saha khouya, rani mzaroub nrouh lih doka, chokran bezaf." },
      { role: "operator", text: "bla mzia, salam." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "unknown",
    id: "SYN_accident_pedestrian_001__00009",
    turns: [
      { role: "operator", text: "l'7imaya l'madaniya f l'istima3." },
      { role: "caller", text: "..." },
      { role: "operator", text: "allo? m3akoum l'7imaya, dachu yellan?" },
      { role: "caller", text: "[bruit de rue] ... attention le piéton! ya khouya wesh bik ... avance chwiya ..." },
      { role: "operator", text: "allo? est-ce que kayen urgence a sidi?" },
      { role: "caller", text: "[bruit de klaxon] ... wesh bik hbesst hna f wost l'abrid, rak dert circulation! ..." },
      { role: "operator", text: "allo, rak f l'7imaya l'madaniya, bon, rani ncoupi, appel silencieux." },
    ]
  },
  {
    type: "❓ Fausse alerte",
    incident: "unknown",
    location: "Aït-Smail",
    id: "SYN_accident_pedestrian_001__00010",
    turns: [
      { role: "caller", text: "allo!" },
      { role: "operator", text: "oui l'7imaya l'madaniya." },
      { role: "caller", text: "khouya rani f aït-smail, kayen wahed l'plaque ta3 piéton tahet f l'abrid, fiha danger kbir, les voitures ygedrou ydirou accident, balak yrenversiw kach wahed." },
      { role: "operator", text: "la plaque tahet f l'abrid? est-ce que kayen accident wela mazal?" },
      { role: "caller", text: "non ma kayench accident, mais lazm tjiw tne7iwha 9bel ma ykoun un piéton darbouh." },
      { role: "operator", text: "d'accord a khouya, nsignaliwha l les travaux publics wela la gendarmerie, hna ul nne7i ula les plaques." },
      { role: "caller", text: "d'accord khouya, fissa s'il vous plaît." },
    ]
  },
];