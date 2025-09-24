import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np

df_original=pd.read_csv('survey_cleaned.csv' , sep=';')
df = df_original.copy()

st.title('Ankieta powitalna wyniki 🚀 ')
st.set_page_config(page_title="Analiza uczestników ankiety", layout="centered")

hobby_cols = [col for col in df.columns if col.startswith("hobby_")]
learning_cols = [col for col in df.columns if col.startswith("learning_pref_")]
motivation_cols = [col for col in df.columns if col.startswith("motivation_")]


motivation_labels = {


    "motivation_career": "Rozwój kariery zawodowej",
    "motivation_challenges": "Możliwość nowych wyzwań",
    "motivation_creativity_and_innovation": "Rozwój kreatywności i innowacyjność",
    "motivation_money_and_job": "Kwestie finansowe i możliwość znalezienia nowej pracy",
    "motivation_personal_growth": "Rozwój osobisty",
    "motivation_remote": "Możliwość pracy zdalnej"
}

learning_labels = {


    "learning_pref_books": "Czytanie książek",
    "learning_pref_chatgpt": "Praca z Chatgpt",
    "learning_pref_offline_courses": "Kursy stacjonarne",
    "learning_pref_online_courses": "Kursy online",
    "learning_pref_personal_projects": "Projekty osobiste",
    "learning_pref_teaching": "Uczenie innych",
    "learning_pref_teamwork": "Praca w zespole",
    "learning_pref_workshops": "Warsztaty tematyczne"
}

hobby_labels = {


    "hobby_art": "Sztuka",
    "hobby_books": "Czytanie książek",
    "hobby_movies": "Oglądanie filmów",
    "hobby_other": "Inne hobby",
    "hobby_sport": "Sport",
    "hobby_video_games": "Gry komputerowe"
}

def create_industry_hobby_correlation():


    hobby_cols = [col for col in df.columns if col.startswith("hobby_")]


    hobby_labels = {
        "hobby_art": "Sztuka",
        "hobby_books": "Czytanie książek", 
        "hobby_movies": "Oglądanie filmów",
        "hobby_other": "Inne hobby",
        "hobby_sport": "Sport",
        "hobby_video_games": "Gry komputerowe"
    }
    
    correlation_data = []
    
    for industry in df['industry'].unique():
        if pd.notna(industry): 
            industry_data = df[df['industry'] == industry]
            row = {'industry': industry}
            
            for hobby_col in hobby_cols:
                hobby_percentage = industry_data[hobby_col].mean() * 100
                hobby_name = hobby_labels.get(hobby_col, hobby_col)
                row[hobby_name] = hobby_percentage
            
            correlation_data.append(row)
    
    corr_df = pd.DataFrame(correlation_data)
    corr_df.set_index('industry', inplace=True)
    
    return corr_df

def create_filter_title():
    filters = []
    
    if age_categories:
        filters.append(f"Wiek: {', '.join(map(str, age_categories))}")
    
    if edu_level_categories:
        filters.append(f"Wykształcenie: {', '.join(edu_level_categories)}")
    
    if industry_categories:
        filters.append(f"Branża: {', '.join(industry_categories)}")
    
    if years_categories:
        filters.append(f"Doświadczenie: {', '.join(map(str, years_categories))}")
    
    if selected_hobbies:
        hobby_names = [hobby_labels.get(h, h) for h in selected_hobbies]
        filters.append(f"Hobby: {', '.join(hobby_names)}")
    
    if learning_preferations:
        learning_names = [learning_labels.get(l, l) for l in learning_preferations]
        filters.append(f"Nauka: {', '.join(learning_names)}")
    
    if motivation_preferations:
        motivation_names = [motivation_labels.get(m, m) for m in motivation_preferations]
        filters.append(f"Motywacja: {', '.join(motivation_names)}")
    
    if place_preferations:
        filters.append(f"Ulubione miejsce spędzania czasu: {', '.join(place_preferations)}")


    if gender != "Wszyscy":
        filters.append(f"Płeć: {gender}")
    
    if filters:
        return f"Rozkład branż ankietowanych po zastosowanych filtrach:\n {' | '.join(filters)}"
    else:
        return "Brak zastosowanych filtrów - wszystkie dane"


def create_age_place_correlation():
    
    df_clean = df[(df['age'] != 'unknown') & (df['fav_place'].notna())].copy()
    crosstab = pd.crosstab(df_clean['age'], df_clean['fav_place'], normalize='index') * 100
    age_order = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", ">=65"]
    existing_ages = [age for age in age_order if age in crosstab.index]
    crosstab = crosstab.reindex(existing_ages)
    
    return crosstab


def create_age_motivation_correlation():
    
    motivation_cols = [col for col in df.columns if col.startswith("motivation_")]


    motivation_labels = {
        "motivation_career": "Rozwój kariery zawodowej",
        "motivation_challenges": "Możliwość nowych wyzwań", 
        "motivation_creativity_and_innovation": "Rozwój kreatywności i innowacyjność",
        "motivation_money_and_job": "Kwestie finansowe i możliwość znalezienia nowej pracy",
        "motivation_personal_growth": "Rozwój osobisty",
        "motivation_remote": "Możliwość pracy zdalnej"
    }
    
    df_clean = df[df['age'] != 'unknown'].copy()
    correlation_data = []
    age_order = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", ">=65"]
    existing_ages = [age for age in age_order if age in df_clean['age'].unique()]
    
    for age_group in existing_ages:
        age_data = df_clean[df_clean['age'] == age_group]
        row = {'age_group': age_group}
        
        for motivation_col in motivation_cols:
            motivation_percentage = age_data[motivation_col].mean() * 100
            motivation_name = motivation_labels.get(motivation_col, motivation_col)
            row[motivation_name] = motivation_percentage
        
        correlation_data.append(row)
    corr_df = pd.DataFrame(correlation_data)
    corr_df.set_index('age_group', inplace=True)
    
    return corr_df


with st.sidebar:
   
    age_categories = st.multiselect(
        'Wybierz kategorię wiekową', sorted(df["age"].dropna().unique())
        )
    
    edu_level_categories = st.multiselect(
        'Wybierz poziom wykształcenia', sorted(df["edu_level"].dropna().unique())
        )
    
    industry_categories = st.multiselect(
        'Wybierz branżę', sorted(df["industry"].dropna().unique())
        )
    
    years_categories = st.multiselect(
        'Wybierz ilość lat doświadczenia w zawodzie', sorted(df["years_of_experience"].dropna().unique())
        )
    
    selected_hobbies = st.sidebar.multiselect(
    "Wybierz hobby",
    options=hobby_cols,
    format_func=lambda x: hobby_labels.get(x, x)
    )   


    learning_preferations = st.sidebar.multiselect(
    "Wybierz preferowany sposób nauki",
    options=learning_cols,
    format_func=lambda x: learning_labels.get(x, x)
    )   


    motivation_preferations = st.sidebar.multiselect(
    "Wybierz motywację podjęcia kursu",
    options=motivation_cols,
    format_func=lambda x: motivation_labels.get(x, x)
    ) 


    place_preferations = st.multiselect(
        'Wybierz ulubione miejsce do spędzania czasu', sorted(df["fav_place"].dropna().unique())
        ) 


    gender = st.radio(
        "Wybierz płeć",
        ["Wszyscy", "Mężczyźni", "Kobiety"],
    )


if age_categories:
    df = df[df["age"].isin(age_categories)]


if edu_level_categories:
    df = df[df["edu_level"].isin(edu_level_categories)]


if industry_categories:
    df = df[df["industry"].isin(industry_categories)]


if place_preferations:
    df = df[df["fav_place"].isin(place_preferations)]


if years_categories:
    df = df[df["years_of_experience"].isin(years_categories)]


if selected_hobbies:
    mask = df[selected_hobbies].all(axis=1)
    df = df[mask]


if learning_preferations:
    mask = df[learning_preferations].all(axis=1)
    df = df[mask]


if motivation_preferations:
    mask = df[motivation_preferations].all(axis=1)
    df = df[mask]


if gender == "Mężczyźni":
    df = df[df["gender"] == 0]


elif gender == "Kobiety":
    df = df[df["gender"] == 1]


c0, c1, c2, c3 = st.columns(4)
with c0:
    st.metric("Liczba ankietowanych", df.shape[0])


with c1:
    st.metric("Liczba mężczyzn", df[df["gender"] == 0 ].shape[0])


with c2:
    st.metric("Liczba kobiet", df[df["gender"] == 1 ].shape[0])


with c3:
    st.metric("Brak informacji", df[df["age"] == "unknown" ].shape[0] or df[df["gender"] == "Nan" ].shape[0])  


x = min(10, len(df))
st.write(f"## {x} losowych wierszy")
st.dataframe(df.sample(x), use_container_width=True, hide_index=True)


if df.empty or df.shape[0] == 0  :
    st.warning("⚠️ Brak danych spełniających wybrane kryteria.")
    st.info("Spróbuj usunąć ostatnio dodany filtr lub zmień inne kryteria.")

else : 

    st.header("Wszystkie wykresy są interaktywne ✨ \n Aby poznać wybraną grupę ankietowanych, 🔄 Skorzystaj z filtrów dostępnych na pasku bocznym")
    age_counts = df["age"].value_counts()
    age_counts = age_counts[age_counts.index != "unknown"]
    age_order = ["<18", "18-24", "25-34", "35-44", "45-54", "55-64", ">=65"]
    existing_ages = [age for age in age_order if age in age_counts.index]
    age_counts = age_counts.reindex(existing_ages)
    existing_ages = [age for age in age_order if age in age_counts.index]
    age_counts = age_counts.reindex(existing_ages)


    fig, ax = plt.subplots(figsize=(10, 6))
    age_counts.plot(kind="bar", ax=ax, color="royalblue")
    ax.set_xlabel("Kategoria wiekowa", fontsize=14,labelpad=10)
    ax.set_ylabel("Liczba ankietowanych", fontsize=14, labelpad=10)
    ax.set_title("Rozkład wieku wśród ankietowanych", fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig)


    edu_counts = df["edu_level"].value_counts()
    fig0, ax = plt.subplots(figsize=(10, 6))
    edu_counts.plot(kind="bar", ax=ax, color="royalblue")
    ax.set_xlabel("Poziom wykształcenia", fontsize=14,labelpad=10)
    ax.set_ylabel("Liczba ankietowanych", fontsize=14, labelpad=10)
    ax.set_title("Rozkład wykształcenia", fontsize=16, fontweight='bold', pad=20)
    plt.xticks(rotation=45, ha='center', fontsize=12)
    plt.yticks(fontsize=12)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig0)

    corr_df = create_industry_hobby_correlation()
    if not (corr_df.empty or corr_df.shape[0] == 0 or corr_df.shape[1] == 0):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            corr_df,
            annot=True,
            fmt='.1f',
            cmap='RdYlBu_r',
            center=50,        
            cbar_kws={'label': 'Procent osób [%]'},
            ax=ax,
            linewidths=0.5
        )
        ax.set_title("Macierz korelacji obecna branża a posiadane hobby ", fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Zainteresowania', fontsize=14, fontweight='bold')
        ax.set_ylabel('Branża', fontsize=14, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)

        st.subheader("Najciekawsze obserwacje ✨ :")
        max_values = corr_df.max()
        max_industries = corr_df.idxmax()

        insights = []
        for hobby, max_val in max_values.items():
            industry = max_industries[hobby]
            insights.append(f"**{hobby}**: najczęściej w branży '{industry}' ({max_val:.1f}%)")

        for insight in insights:
            st.write(f"• {insight}\n")

    place_corr = create_age_place_correlation()
    if not (place_corr.empty or place_corr.shape[0] == 0 or place_corr.shape[1] == 0):
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(
            place_corr,
            annot=True,
            fmt='.1f',
            cmap='viridis',
            cbar_kws={'label': 'Procent w grupie wiekowej [%]'},
            ax=ax,
            linewidths=0.5
        )

        ax.set_title('Preferencje spędzania czasu według grup wiekowych', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Ulubione miejsce', fontsize=14, fontweight='bold')
        ax.set_ylabel('Grupa wiekowa', fontsize=14, fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        st.pyplot(fig)

    motivation_corr = create_age_motivation_correlation()
    if not (motivation_corr.empty or motivation_corr.shape[0] == 0 or motivation_corr.shape[1] == 0):
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.heatmap(
            motivation_corr,
            annot=True,
            fmt='.1f',
            cmap='RdYlBu_r',  
            center=50,        
            cbar_kws={'label': 'Procent osób w grupie wiekowej [%]'},
            ax=ax,
            linewidths=0.5
        )

        ax.set_title('Motywacja podjęcia kursu według grup wiekowych', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Motywacja podjęcia kursu', fontsize=14, fontweight='bold')
        ax.set_ylabel('Grupa wiekowa', fontsize=14, fontweight='bold')

        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        st.pyplot(fig)

        st.subheader("Obserwacje dotyczące motywacji ✨ :")
        insights = []

        for motivation in motivation_corr.columns:
            max_age = motivation_corr[motivation].idxmax()
            max_val = motivation_corr[motivation].max()
            min_age = motivation_corr[motivation].idxmin()
            min_val = motivation_corr[motivation].min()
            
            if max_val - min_val > 15: 
                insights.append(f"**{motivation}**: najczęściej w grupie {max_age} ({max_val:.1f}%), najrzadziej w grupie {min_age} ({min_val:.1f}%)")

        if insights:
            st.write("**Największe różnice między grupami wiekowymi:**")
            for insight in insights:
                st.write(f"• {insight}")
        else:
            st.write("Motywacje są stosunkowo równomiernie rozłożone między grupami wiekowymi.")

        if not motivation_corr.empty:
            ranges = motivation_corr.max() - motivation_corr.min()
            most_varied = ranges.idxmax()
            
            st.subheader(f"Szczegółowy rozkład: {most_varied}")
            
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            motivation_corr[most_varied].plot(kind='bar', ax=ax2, color='steelblue')
            
            ax2.set_title(f'{most_varied} - rozkład według wieku', fontsize=14, fontweight='bold')
            ax2.set_xlabel('Grupa wiekowa', fontsize=12)
            ax2.set_ylabel('Procent osób [%]', fontsize=12)
            ax2.grid(True, alpha=0.3, axis='y')
            
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            st.pyplot(fig2)


    st.subheader("Liczebności ankietowanych w danej branży od filtrów 😊 ")
 
    fig, ax = plt.subplots(figsize=(16, 10))
    industry_counts = df["industry"].value_counts()


    if len(industry_counts) == 0:
            st.warning("⚠️ Brak danych o branżach dla wybranych filtrów.")
    else:
                
                industry_counts.plot(kind="bar", ax=ax)
                title = create_filter_title()
                ax.set_title(title, fontsize=16, fontweight='bold', pad=30, linespacing=1.5)
                ax.set_xlabel("Branża", fontsize=14, fontweight='bold', labelpad=15)
                ax.set_ylabel("Liczba ankietowanych", fontsize=14, fontweight='bold', labelpad=15)
                plt.xticks(rotation=45, ha='right', fontsize=12)
                plt.yticks(fontsize=12)
                ax.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.subplots_adjust(bottom=0.15)
                st.pyplot(fig)


    st.download_button(
    label="📥 Pobierz aktualnie przefiltrowane dane z wykresu -  format ( CSV )",
    data=df.to_csv(index=False, sep=';'),
    file_name='wyniki_ankiety.csv',
    mime='text/csv'
)
