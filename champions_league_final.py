import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import os

############# Data ##############################

base_path = os.path.dirname(__file__)
relative_path = 'champions_data.xlsx'
full_path = os.path.join(base_path,relative_path)

relative_path_1 = 'champions_stat_logs.xlsx'
full_path_1 = os.path.join(base_path,relative_path_1)

df = pd.read_excel(full_path,sheet_name='Sheet7')
df1 = pd.read_excel(full_path_1,sheet_name='Sheet1')
df2 = pd.read_excel(full_path_1,sheet_name='Sheet2')
df3 = pd.read_excel(full_path_1,sheet_name='Sheet3')

df4 = pd.read_excel(full_path, sheet_name='Sheet15')

madrid_competition = df[(df['Comp'] == 'Champions Lg') & (df['Round'] != 'Final')]
madrid_shooting = df1[(df1['Comp'] == 'Champions Lg') & (df1['Round'] != 'Final') & (df1['Team'] == "Real Madrid")]
madrid_passing = df2[(df2['Comp'] == 'Champions Lg') & (df2['Round'] != 'Final') & (df1['Team'] == "Real Madrid")]
madrid_defense = df3[(df3['Comp'] == 'Champions Lg') & (df3['Round'] != 'Final') & (df1['Team'] == "Real Madrid")]

dortmund_competition = df4[(df4['Comp'] == 'Champions Lg') & (df4['Round'] != 'Final')]
dortmund_shooting = df1[(df1['Comp'] == 'Champions Lg') & (df1['Round'] != 'Final') & (df1['Team'] == "Dortmund")]
dortmund_passing = df2[(df2['Comp'] == 'Champions Lg') & (df2['Round'] != 'Final') & (df1['Team'] == "Dortmund")]
dortmund_defense = df3[(df3['Comp'] == 'Champions Lg') & (df3['Round'] != 'Final') & (df1['Team'] == "Dortmund")]

GF_total = int(madrid_competition['GF'].sum())
GA_total = int(madrid_competition['GA'].sum())
avg_pos = round(madrid_competition['Poss'].mean(),1)
avg_gol_game = round(madrid_competition['GF'].mean(),1)
avg_gol_against = round(madrid_competition['GA'].mean(),1)

GF_total_dortmund = int(dortmund_competition['GF'].sum())
GA_total_dortmund = int(dortmund_competition['GA'].sum())
avg_pos_dortmund = round(dortmund_competition['Poss'].mean(),1)
avg_gol_game_dortmund = round(dortmund_competition['GF'].mean(),1)
avg_gol_against_dortmund = round(dortmund_competition['GA'].mean(),1)

############# Streamlit #########################

st.set_page_config(layout="wide")

st.title('Champions league 23/24 - análisis de la final (prepartido) ', anchor=None)


selected = option_menu(None, ["Real Madrid", "Borussia Dortmund"],  
        menu_icon="cast", default_index=0, orientation="horizontal")

if selected == "Real Madrid":
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        container = st.container(border=True)
        container.subheader('Total goles a favor')
        container.subheader(f'{GF_total}')
    
    with col2:
        container = st.container(border=True)
        container.subheader('Total goles en contra')
        container.subheader(f'{GA_total}')
       
    with col3:
        container = st.container(border=True)
        container.subheader('Posesión promedio')
        container.subheader(f'{avg_pos} %')
        
    col4,col5 = st.columns(2)
    
    with col4:
        container = st.container(border=True)
        container.subheader('Promedio de gol por partido')
        container.subheader(f'{avg_gol_game}')
        
    with col5:
        container = st.container(border=True)
        container.subheader('Promedio de gol en contra por partido')
        container.subheader(f'{avg_gol_against}')  
    
    with st.expander("Remates"):
        competiciones = st.selectbox(
            "Ronda",
            options= madrid_shooting["Round"].unique(),
            key=0,       
        )
        
        df_selection = madrid_shooting.query("Round == @competiciones")
        
        data_madrid = df_selection[(df_selection['ForAgainst'] == 'For')]        
       
        g_minus_xg = round(data_madrid['G_minus_xG_Expected'].sum(),1)
        g_minus_xg_np = round(data_madrid['np:G_minus_xG_Expected'].sum(),1)
        
        def color_text(value):
            if value < 0:
                color = "red"
            else:
                color = "green"
            return f"<span style='color:{color}'>{value}</span>"   
            
        col6,col7 = st.columns(2)
        
        with col6:
            container = st.container(border=True)
            container.markdown(f"{color_text(g_minus_xg)}", unsafe_allow_html=True)
            container.caption("Goles - Goles esperados")
        
        with col7:
            container = st.container(border=True)      
            container.markdown(f"{color_text(g_minus_xg_np)}", unsafe_allow_html=True)
            container.caption("Goles - Goles esperados (excluyendo penaltis)")          
            
        col8,col9,col10,col11 = st.columns(4)
        
        with col8:
            goals = px.bar(
                df_selection,
                x="Date",
                y="Gls_Standard",
                title="Goles a favor (for) vs Goles en contra (against)",
                width=400,
                height=400,
                color="ForAgainst",
                barmode="group",
                text_auto=True,
                color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                hover_data=['Opponent'],
            )
            
            goals.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
                        
            st.plotly_chart(goals, use_container_width=True)
                
        with col9:            
            shoots = px.pie(
                df_selection,
                values="Sh_Standard",
                names="ForAgainst",
                title="Remates - sin incluir penaltis<br> a favor (for) y en contra (against)",
                width=400,
                height=400,
                color="ForAgainst",
                color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                hover_data=['Opponent'],
            )
                
            st.plotly_chart(shoots, use_container_width=True)
        
        with col10:
            sot = px.bar(df_selection,x="Date", y="SoT_Standard", color="ForAgainst", hover_data=['Opponent'], title="Remates a puerta - sin incluir penaltis<br> a favor (for) y en contra (against)"
                               ,barmode="group", width=400, height=400,text_auto=True,color_discrete_map={"For":"#00529F","Against":"#EE324E"})
            
            sot.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )            
            
            st.plotly_chart(sot, use_container_width=True)
            
        with col11:    
            goals_per_sot = px.bar(df_selection, x="Date", y="G_per_SoT_Standard", color="ForAgainst", hover_data=['Opponent']
                                   , title="Goles por remate a porteria <br>- sin incluir penaltis a favor (for) y en <br>contra (against)", barmode="group", width=400, height=400,text_auto=True,
                                   color_discrete_map={"For":"#00529F","Against":"#EE324E"})
            
            goals_per_sot.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )            

            st.plotly_chart(goals_per_sot, use_container_width=True)
                       
    with st.expander("Pases"):
        competiciones = st.selectbox(
            "Ronda",
            options= madrid_passing["Round"].unique(),
            key=1,        
        )
        
        df_selection = madrid_passing.query("Round == @competiciones")
        
        data_madrid_pases = df_selection[(df_selection['ForAgainst'] == 'For')]
        
        asistencias_totales = int(data_madrid_pases['Ast'].sum()) 
        pases_clave = int(data_madrid_pases['KP'].sum())
        centros = int(data_madrid_pases['CrsPA'].sum())
        
        
        col12,col13,col14 = st.columns(3)
        
        with col12:
            container = st.container(border=True)
            container.markdown(f"{asistencias_totales}")
            container.caption("Asistencias totales")
        
        with col13:
            container = st.container(border=True)
            container.markdown(f"{pases_clave}")
            container.caption("Pases clave")
            
        with col14:
            container = st.container(border=True)
            container.markdown(f"{centros}")
            container.caption('Centros')
            
        col15,col16,col17,col18 = st.columns(4)
        
        with col15:
            pases_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Total',
                  color="ForAgainst",
                  color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                  title="Pases completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400
                  )
            
            st.plotly_chart(pases_completos, use_container_width=True)
            
        with col16:
            pases_cortos_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Short',
                  color="ForAgainst",
                  color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                  title="Pases cortos completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400,
                  )
            
            st.plotly_chart(pases_cortos_completos, use_container_width=True)
            
        with col17:
            pases_medios_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Medium',
                  color="ForAgainst",
                  color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                  title="Pases medios completos <br>a favor (for) y en contra (against)",
                  height=400,
                  width=400,
                  )
            
            st.plotly_chart(pases_medios_completos, use_container_width=True)
        
        with col18:
            pases_largos_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Long',
                  color="ForAgainst",
                  color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                  title="Pases largos completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400,
                  )           

            st.plotly_chart(pases_largos_completos, use_container_width=True)        
    
    with st.expander("Defensa"):    
        competiciones = st.selectbox(
            "Ronda",
            options= madrid_defense["Round"].unique(),        
            key=2,
        )
        
        df_selection = madrid_defense.query("Round == @competiciones")
            
        data_madrid_defensa = df_selection[(df_selection['ForAgainst'] == 'For')]
        
        intercepciones = int(data_madrid_defensa['Int'].sum())
        despejes = int(data_madrid_defensa['Clr'].sum())
        errores = int(data_madrid_defensa['Err'].sum())  

        col19,col20,col21 = st.columns(3)
        
        with col19:
            container = st.container(border=True)
            container.markdown(f"{intercepciones}")
            container.caption("Intercepciones totales")
            
        with col20:
            container = st.container(border=True)
            container.markdown(f"{despejes}")
            container.caption("Despejes totales totales")
        
        with col21:
            container = st.container(border=True)
            container.markdown(f"{errores}")
            container.caption("Errores totales")

        col22,col23,col24 = st.columns(3)
        
        with col22:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Def 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                text_auto=True,
                title="Entradas en zona defensiva <br>a favor (for) y en contra (against)"
            )

            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )

            st.plotly_chart(fig,use_container_width=True)
            
        with col23:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Mid 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                text_auto=True,
                title="Entradas en medio campo <br>a favor (for) y en contra (against)"
            )

            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
        
            st.plotly_chart(fig,use_container_width=True)
            
        with col24:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Att 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#00529F","Against":"#EE324E"},
                text_auto=True,
                title="Entradas en zona de ataque <br>a favor (for) y en contra (against)"
            )
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
    
            st.plotly_chart(fig, use_container_width=True)
           
    
    
if selected == "Borussia Dortmund":
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        container = st.container(border=True)
        container.subheader('Total goles a favor')
        container.subheader(f'{GF_total_dortmund}')
    
    with col2:
        container = st.container(border=True)
        container.subheader('Total goles en contra')
        container.subheader(f'{GA_total_dortmund}')
       
    with col3:
        container = st.container(border=True)
        container.subheader('Posesión promedio')
        container.subheader(f'{avg_pos_dortmund} %')
        
    col4,col5 = st.columns(2)
    
    with col4:
        container = st.container(border=True)
        container.subheader('Promedio de gol por partido')
        container.subheader(f'{avg_gol_game_dortmund}')
        
    with col5:
        container = st.container(border=True)
        container.subheader('Promedio de gol en contra por partido')
        container.subheader(f'{avg_gol_against_dortmund}') 
    
    with st.expander("Remates"):
        competiciones = st.selectbox(
            "Ronda",
            options= dortmund_shooting["Round"].unique(),
            key=0,       
        )
        
        df_selection = dortmund_shooting.query("Round == @competiciones")
        
        data_dortmund = df_selection[(df_selection['ForAgainst'] == 'For')]        
       
        g_minus_xg_dortmund = round(data_dortmund['G_minus_xG_Expected'].sum(),1)
        g_minus_xg_np_dortmund = round(data_dortmund['np:G_minus_xG_Expected'].sum(),1)
        
        def color_text(value):
            if value < 0:
                color = "red"
            else:
                color = "green"
            return f"<span style='color:{color}'>{value}</span>"   
            
        col6,col7 = st.columns(2)
        
        with col6:
            container = st.container(border=True)
            container.markdown(f"{color_text(g_minus_xg_dortmund)}", unsafe_allow_html=True)
            container.caption("Goles - Goles esperados")
        
        with col7:
            container = st.container(border=True)      
            container.markdown(f"{color_text(g_minus_xg_np_dortmund)}", unsafe_allow_html=True)
            container.caption("Goles - Goles esperados (excluyendo penaltis)")          
            
        col8,col9,col10,col11 = st.columns(4)
        
        with col8:
            goals = px.bar(
                df_selection,
                x="Date",
                y="Gls_Standard",
                title="Goles a favor (for) <br>vs Goles en contra (against)",
                color="ForAgainst",
                barmode="group",
                text_auto=True,
                color_discrete_map={"For":"#FDE100","Against":"#000000"},
                hover_data=['Opponent'],
            )
            
            goals.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
            
            st.plotly_chart(goals, use_container_width=True)
                
        with col9:            
            shoots = px.pie(
                df_selection,
                values="Sh_Standard",
                names="ForAgainst",
                title="Remates - sin incluir penaltis <br>a favor (for) y en contra (against)",
                color="ForAgainst",
                color_discrete_map={"For":"#FDE100","Against":"#000000"},
                hover_data=['Opponent'],
            )
            
            shoots.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
    
            st.plotly_chart(shoots,use_container_width=True)
        
        with col10:
            sot = px.bar(df_selection,x="Date", y="SoT_Standard", color="ForAgainst", hover_data=['Opponent'], title="Remates a puerta - sin incluir penaltis <br>a favor (for) y en contra (against)"
                               ,barmode="group", width=400, height=400,text_auto=True,color_discrete_map={"For":"#FDE100","Against":"#000000"})
            
            sot.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )

            st.plotly_chart(sot, use_container_width=True)
            
        with col11:    
            goals_per_sot = px.bar(df_selection, x="Date", y="G_per_SoT_Standard", color="ForAgainst", hover_data=['Opponent']
                                   , title="Goles por remate a porteria <br>- sin incluir penaltis a favor (for) y <br>en contra (against)", barmode="group", width=400, height=400,text_auto=True,
                                   color_discrete_map={"For":"#FDE100","Against":"#000000"})
            
            goals_per_sot.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )            

            st.plotly_chart(goals_per_sot, use_container_width=True)
            
    with st.expander("Pases"):
        competiciones = st.selectbox(
            "Ronda",
            options= dortmund_passing["Round"].unique(),
            key=1,        
        )
        
        df_selection = dortmund_passing.query("Round == @competiciones")
        
        data_dortmund_pases = df_selection[(df_selection['ForAgainst'] == 'For')]
        
        asistencias_totales_dortmund = int(data_dortmund_pases['Ast'].sum()) 
        pases_clave_dortmund = int(data_dortmund_pases['KP'].sum())
        centros_dortmund = int(data_dortmund_pases['CrsPA'].sum())
        
        
        col12,col13,col14 = st.columns(3)
        
        with col12:
            container = st.container(border=True)
            container.markdown(f"{asistencias_totales_dortmund}")
            container.caption("Asistencias totales")
        
        with col13:
            container = st.container(border=True)
            container.markdown(f"{pases_clave_dortmund}")
            container.caption("Pases clave")
            
        with col14:
            container = st.container(border=True)
            container.markdown(f"{centros_dortmund}")
            container.caption('Centros')
            
        col15,col16,col17,col18 = st.columns(4)
        
        with col15:
            pases_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Total',
                  color="ForAgainst",
                  color_discrete_map={"For":"#FDE100","Against":"#000000"},
                  title="Pases completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400
                  )
            
            st.plotly_chart(pases_completos, use_container_width=True)
            
        with col16:
            pases_cortos_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Short',
                  color="ForAgainst",
                  color_discrete_map={"For":"#FDE100","Against":"#000000"},
                  title="Pases cortos completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400,
                  )
            
            st.plotly_chart(pases_cortos_completos, use_container_width=True)
            
        with col17:
            pases_medios_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Medium',
                  color="ForAgainst",
                  color_discrete_map={"For":"#FDE100","Against":"#000000"},
                  title="Pases medios completos <br>a favor (for) y en contra (against)",
                  height=400,
                  width=400,
                  )
            
            st.plotly_chart(pases_medios_completos, use_container_width=True)
        
        with col18:
            pases_largos_completos = px.sunburst(df_selection, path=['ForAgainst','Opponent'],values='Cmp_Long',
                  color="ForAgainst",
                  color_discrete_map={"For":"#FDE100","Against":"#000000"},
                  title="Pases largos completos <br>a favor (for) y en contra (against)",
                  width=400,
                  height=400,
                  )

            
            st.plotly_chart(pases_largos_completos, use_container_width=True)        
                    
    with st.expander("Defensa"):    
        competiciones = st.selectbox(
            "Ronda",
            options= dortmund_defense["Round"].unique(),        
            key=2,
        )
        
        df_selection = dortmund_defense.query("Round == @competiciones")
            
        data_dortmund_defensa = df_selection[(df_selection['ForAgainst'] == 'For')]
        
        intercepciones_dortmund = int(data_dortmund_defensa['Int'].sum())
        despejes_dortmund = int(data_dortmund_defensa['Clr'].sum())
        errores_dortmund = int(data_dortmund_defensa['Err'].sum())  

        col19,col20,col21 = st.columns(3)
        
        with col19:
            container = st.container(border=True)
            container.markdown(f"{intercepciones_dortmund}")
            container.caption("Intercepciones totales")
            
        with col20:
            container = st.container(border=True)
            container.markdown(f"{despejes_dortmund}")
            container.caption("Despejes totales totales")
        
        with col21:
            container = st.container(border=True)
            container.markdown(f"{errores_dortmund}")
            container.caption("Errores totales")

        col22,col23,col24 = st.columns(3)
        
        with col22:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Def 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#FDE100","Against":"#000000"},
                text_auto=True,
                title="Entradas en zona defensiva <br>a favor (for) y en contra (against)"
            )
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col23:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Mid 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#FDE100","Against":"#000000"},
                text_auto=True,
                title="Entradas en medio campo <br>a favor (for) y en contra (against)"
            )
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )            
            
            st.plotly_chart(fig,use_container_width=True)
            
        with col24:
            fig = px.bar(
                df_selection,
                x='Date',
                y='Att 3rd_Tackles',
                barmode='group',
                color='ForAgainst',
                height=450,
                width=450,
                color_discrete_map={"For":"#FDE100","Against":"#000000"},
                text_auto=True,
                title="Entradas en zona de ataque <br>a favor (for) y en contra (against)"
            )
            
            fig.update_layout(
                xaxis=dict(showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False, zeroline=False)
                )
                        
            st.plotly_chart(fig, use_container_width=True)
               
