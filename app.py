import pandas as pd
from shiny import App, ui
from shinywidgets import output_widget, render_widget
import plotly.express as px
from pathlib import Path

css_path = Path(__file__).parent / "styl.css"

app_languages = ["Polish", "English", "Chinese"]

# Słowniki służą w celu stworzenia czytelnych elementów select
language_names_polish = {'ARA': 'Arabski', 'BUL': 'Bułgarski', 'CHI': 'Chiński', 'CZE': 'Czeski', 'DAN': 'Duński', 'DUT': 'Holenderski; Flamandzki', 'ENG': 'Angielski', 'EST': 'Estoński', 'FIN': 'Fiński', 'FRE': 'Francuski', 'GER': 'Niemiecki', 'GLE': 'Irlandzki', 'GRE': 'Grecki', 'HRV': 'Chorwacki', 'HUN': 'Węgierski', 'ITA': 'Włoski', 'JPN': 'Japoński', 'LAV': 'Łotewski', 'LIT': 'Litewski', 'MLT': 'Maltański', 'OTH': 'Inny', 'POL': 'Polski', 'POR': 'Portugalski', 'RUM': 'Rumuński', 'RUS': 'Rosyjski', 'SLO': 'Słowacki', 'SLV': 'Słoweński', 'SPA': 'Hiszpański', 'SWE': 'Szwedzki', 'UNK': 'Nieznany'}
country_names_polish = {'AT': 'Austria', 'BA': 'Bośnia i Hercegowina', 'BE': 'Belgia', 'BE_FRA': 'Wspólnota Francuska w Belgii', 'BE_VLA': 'Wspólnota Flamandzka w Belgii', 'BG': 'Bułgaria', 'CY': 'Cypr', 'CZ': 'Czechy', 'DE': 'Niemcy', 'DK': 'Dania', 'EE': 'Estonia', 'EL': 'Grecja', 'ES': 'Hiszpania', 'EU27_2020': 'Unia Europejska - 27 krajów (od 2020 r.)', 'EU28': 'Unia Europejska - 28 krajów (2013-2020 r.)', 'FI': 'Finlandia', 'FR': 'Francja', 'HR': 'Chorwacja', 'HU': 'Węgry', 'IE': 'Irlandia', 'IS': 'Islandia', 'IT': 'Włochy', 'LI': 'Liechtenstein', 'LT': 'Litwa', 'LU': 'Luksemburg', 'LV': 'Łotwa', 'MK': 'Północna Macedonia', 'MT': 'Malta', 'NL': 'Holandia', 'NO': 'Norwegia', 'PL': 'Polska', 'PT': 'Portugalia', 'RO': 'Rumunia', 'RS': 'Serbia', 'SE': 'Szwecja', 'SI': 'Słowenia', 'SK': 'Słowacja', 'UK': 'Wielka Brytania'}
# Sortuję zawartość alfabetycznie aby ułatwić nawigowanie po stronie
language_names_polish = dict(sorted(language_names_polish.items(), key=lambda item: item[1]))
country_names_polish = dict(sorted(country_names_polish.items(), key=lambda item: item[1]))
iso3_dict = {'AT': 'AUT', 'BA': 'BIH', 'BE': 'BEL', 'BE_FRA': 'BE_FRA', 'BE_VLA': 'BE_VLA', 'BG': 'BGR', 'CY': 'CYP', 'CZ': 'CZE', 'DE': 'DEU', 'DK': 'DNK', 'EE': 'EST', 'EL': 'GRC', 'ES': 'ESP', 'EU27_2020': 'EU27', 'EU28': 'EU28', 'FI': 'FIN', 'FR': 'FRA', 'HR': 'HRV', 'HU': 'HUN', 'IE': 'IRL', 'IS': 'ISL', 'IT': 'ITA', 'LI': 'LIE', 'LT': 'LTU', 'LU': 'LUX', 'LV': 'LVA', 'MK': 'MKD', 'MT': 'MLT', 'NL': 'NLD', 'NO': 'NOR', 'PL': 'POL', 'PT': 'PRT', 'RO': 'ROU', 'RS': 'SRB', 'SE': 'SWE', 'SI': 'SVN', 'SK': 'SVK', 'UK': 'GBR'}
level_of_education = {"ED1": "Szkoła Podstawowa", "ED2": "Szkoła Gimnazjalna", "ED3": "Szkoła Średnia"}
# Wczytuję pobrany plik csv z danymi
file = Path(__file__).parent / "languages_eu.csv"
df = pd.read_csv(file)
df.drop(df[df['language'] == 'TOTAL'].index, inplace=True)
df['iso3'] = df['geo'].map(iso3_dict)


plots_labels = {"TIME_PERIOD": "rok", "OBS_VALUE": "Odsetek uczniów (%)", "geo": "kraj", "language": "język"}
app_ui = ui.page_fluid(
    # Poniższy kod stanowi odwzorowanie html'owego szkicu
    ui.include_css(css_path),
    ui.div(
        {"class": "header"},
        ui.div(
            {"class": "header-title"},
            "Języki obce wśród europejskich uczniów",
        ),
        ui.div({"class": "podpis"}, "Dominik Klisiewicz 100466" )
        ,
        ui.input_select("level", "",level_of_education),
    ),
    ui.div(
        {"class": "content-frame"},
        ui.div(
            {"class": "map-frame"},
            {"class": "big-card"},
            ui.div(
                # {"class": "big-card"},
                # TUTAJ MAPA
                output_widget("map"),
                            ui.div(
                {"class": "control-panel-big"},
                ui.div(
                    {"class": "card"},
                    {"class": "spc"},
                    ui.input_select("map_language", "Wybierz język", language_names_polish),
                    ui.output_text("map_text")
                ),
                ui.div(
                    {"class": "card"},
                    {"class": "spc"},
                    ui.input_slider("map_year", "", 2013, 2021, 2015, sep=""),
                    ui.input_switch("skala", "Stała skala")
                )

            )
            ),

        ),

        ui.div(
            {"class": "plots-frame"},
            ui.div(
                {"class": "plot-frame-inverse"},
                {"class": "big-card"},
                ui.div(
                    {"class": "control-panel"},
                    ui.div(
                        {"class": "card"},
                        ui.input_select("top_lang_c", "Wybierz Kraj", country_names_polish)
                    ),
                    ui.div(
                        {"class": "card"},
                        ui.input_slider("top_lang_y", "Rok", 2013, 2021, 2020, sep=""),
                        ui.input_switch("skala2", "Stała skala")
                    )
                ),
                ui.div(
                    # TUTAJ TOP JĘZYKI W PAŃSTWIE
                    output_widget("top_languages")
                ),
            ),
            ui.div(
                {"class": "plot-frame"},
                {"class": "big-card"},
                ui.div(
                    output_widget("language_in_country")
                ),
                ui.div(
                        {"class": "card"},
                        ui.input_select("lic_country", "Wybierz Kraj", country_names_polish),
                        ui.input_select("lic_language", "Wybierz Język", language_names_polish),
                        ui.output_text("c")
                    
                ),
            ),

        )

    )
)

def server(input, output, session):

    @output
    @render_widget
    def top_languages():
        # Filtry pod nowy df
        year_filter = df["TIME_PERIOD"]== input.top_lang_y()
        geo_filter = df["geo"]== input.top_lang_c()
        level_filter = df["isced11"]== input.level()
        value_filter = df["OBS_VALUE"] > 0

        filtrd = df[year_filter & geo_filter & level_filter & value_filter][["language", "OBS_VALUE"]].sort_values(by = "OBS_VALUE")
        title = "Najpopularniejsze języki w kraju"
        if filtrd.empty:  # w razie pustego df tytuł wykresu to brak danych
            title = "Brak danych"
        # Utworzenie wykresu słupkowego
        fig = px.bar(filtrd, x="OBS_VALUE", y="language",
                    template="simple_white",
                    labels=plots_labels,
                    title=title)
        if input.skala2():  # doprowadzenie skali legendy do stałych wartości
            fig.update_xaxes(range=[0, 100])
        fig.layout.height = 400
        fig.layout.width = 300
        return fig
    
    @output
    @render_widget
    def language_in_country():
        # Filtry pod nowy df
        geo_filter = df["geo"]== input.lic_country()
        lang_filter = df["language"] == input.lic_language()
        value_filter = df["OBS_VALUE"] > 0
        level_filter = df["isced11"]==input.level()
        filtrd = df[lang_filter & geo_filter & level_filter & value_filter][["TIME_PERIOD", "OBS_VALUE"]]
        title = "Popularność języka w kraju"
        if filtrd.empty:
            title = "Brak danych"
        # Utworzenie wykresu liniowego 
        fig = px.line(filtrd, x="TIME_PERIOD", y="OBS_VALUE",
                    template="simple_white", 
                    labels=plots_labels,
                    title=title,
                    )
        fig.layout.height = 300
        fig.layout.width = 300
        return fig
    
    @output
    @render_widget
    def map():
        # Filtry pod nowy df
        year_filter = df["TIME_PERIOD"]== input.map_year()
        lang_filter = df["language"] == input.map_language()
        level_filter = df["isced11"]== input.level()
        filtrd = df[lang_filter & year_filter & level_filter][["iso3", "OBS_VALUE"]]
        # Utworzenie mapy na podstawie przefiltrowanego df
        fig = px.choropleth(filtrd,
            locations='iso3',
            color='OBS_VALUE',
            locationmode='ISO-3',
            color_continuous_scale=["white", "palegreen", "blue"],
            labels={'OBS_VALUE':'Odsetek uczniów (%)'}
        )
        fig.update_layout(
            title=dict(
                text='Popularność języka w krajach Europy',
                x=.5,
                font_size=18,
                ),
            geo=dict( 
                bgcolor='#FFFFFF',
                lakecolor='#FFFFFF',
                projection_type='miller',
                scope='europe'
                ),
            
            width = 700,
            height = 700,
        )
        if input.skala():  # doprowadzenie skali legendy do stałych wartości
            fig.update_layout(
                coloraxis=dict(
                cmin=0,
                cmax=100, 
                colorbar_tickvals=[0, 25, 50, 75, 100],
                )          
            )

        return fig

app = App(app_ui, server, debug=True)