library(worldfootballR)

man_city <- "https://fbref.com/en/squads/b8fd03ef/Manchester-City-Stats"
copenhagen <- "https://fbref.com/en/squads/18050b20/FC-Copenhagen-Stats"
arsenal <-"https://fbref.com/en/squads/18bb7c10/Arsenal-Stats"
porto <- "https://fbref.com/en/squads/5e876ee6/Porto-Stats"
bayern_munich <-"https://fbref.com/en/squads/054efa67/Bayern-Munich-Stats"
lazio <- "https://fbref.com/en/squads/7213da33/Lazio-Stats"
real_madrid <-"https://fbref.com/en/squads/53a2f082/Real-Madrid-Stats"
leipzig <- "https://fbref.com/en/squads/acbb6a5b/RB-Leipzig-Stats"
barcelona <- "https://fbref.com/en/squads/206d90db/Barcelona-Stats"
napoli <- "https://fbref.com/en/squads/d48ad4ff/Napoli-Stats"
atletico_madrid <- "https://fbref.com/en/squads/db3b9613/Atletico-Madrid-Stats"
inter <- "https://fbref.com/en/squads/d609edc0/Internazionale-Stats"
psg <- "https://fbref.com/en/squads/e2d8892c/Paris-Saint-Germain-Stats"
real_sociedad <-"https://fbref.com/en/squads/e31d1cd9/Real-Sociedad-Stats"
dortmund <-"https://fbref.com/en/squads/add600ae/Dortmund-Stats"
psv <- "https://fbref.com/en/squads/e334d850/PSV-Eindhoven-Stats"

man_city_results <- fb_team_match_results(man_city)
copenhagen_results <- fb_team_match_results(copenhagen)
arsenal_results <- fb_team_match_results(arsenal)
port_results <- fb_team_match_results(porto)
bayern_munich_results <- fb_team_match_results(bayern_munich)
lazio_results <- fb_team_match_results(lazio)
real_madrid_results <- fb_team_match_results(real_madrid)
leipzig_results <- fb_team_match_results(leipzig)
barcelona_results <- fb_team_match_results(barcelona)
napoli_results <- fb_team_match_results(napoli)
atletico_madrid_results <- fb_team_match_results(atletico_madrid)
inter_results <- fb_team_match_results(inter)
psg_results <- fb_team_match_results(psg)
real_sociedad_results <- fb_team_match_results(real_sociedad)
dortmund_results <- fb_team_match_results(dortmund)
psv_results <- fb_team_match_results(psv)


install.packages("openxlsx", dependencies = TRUE)

library(openxlsx)

dataset_names <- list('Sheet1' = man_city_results, 'Sheet2' = copenhagen_results, 'Sheet3' = arsenal_results,
                      'Sheet4' = port_results, 'Sheet5' = bayern_munich_results, 'Sheet6' = lazio_results,
                      'Sheet7' = real_madrid_results, 'Sheet8' = leipzig_results, 'Sheet9' = barcelona_results,
                      'Sheet10' = napoli_results, 'Sheet11' = atletico_madrid_results, 'Sheet12' = inter_results,
                      'Sheet13' = psg_results, 'Sheet14' = real_sociedad_results, 'Sheet15' = dortmund_results,
                      'Sheet16' = psv_results)

openxlsx::write.xlsx(dataset_names, file = "champions_data.xlsx")