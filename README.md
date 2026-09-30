# autoresportuguesesdp
Autores Portugueses em Dominio Público



SELECT DISTINCT ?label ?qid ?wikidataUrl ?wikipediaUrl ?dateOfBirth ?dateOfDeath ?publicDomainYear WHERE {
  ?author wdt:P31 wd:Q5 ;
          wdt:P27 wd:Q45 ;
          wdt:P569 ?dateOfBirth ;
          wdt:P570 ?dateOfDeath ;
          rdfs:label ?label .
  FILTER(LANG(?label) = "pt")

  BIND(STRAFTER(STR(?author), "entity/") AS ?qid)
  BIND(CONCAT("https://www.wikidata.org/wiki/", ?qid) AS ?wikidataUrl)

  # Portuguese Wikipedia article only, with "-" fallback
  OPTIONAL {
    ?wikipediaArticle schema:about ?author ;
                      schema:isPartOf <https://pt.wikipedia.org/> .
  }
  BIND(COALESCE(STR(?wikipediaArticle), "-") AS ?wikipediaUrl)

  BIND(YEAR(?dateOfDeath) + 71 AS ?publicDomainYear)
  FILTER(?publicDomainYear <= 2026)
}
ORDER BY ?label
LIMIT 5000
