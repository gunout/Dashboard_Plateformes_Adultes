# dashboard_platforms_adult_content.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
import random
import warnings
warnings.filterwarnings('ignore')

# Configuration de la page
st.set_page_config(
    page_title="Analyse des Plateformes de Contenu Adulte - Live",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #FF6B6B, #FF8E53, #FF6B6B);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .live-badge {
        background: linear-gradient(45deg, #FF416C, #FF4B2B);
        color: white;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .metric-card {
        background-color: #1e1e1e;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #FF416C;
        margin: 0.5rem 0;
        color: white;
    }
    .section-header {
        color: #FF416C;
        border-bottom: 2px solid #FF416C;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
    }
    .platform-card {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 5px solid;
        background-color: #2d2d2d;
        color: white;
    }
    .creator-card {
        background: linear-gradient(45deg, #2d2d2d, #3d3d3d);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #FF416C;
    }
</style>
""", unsafe_allow_html=True)

class AdultPlatformsDashboard:
    def __init__(self):
        self.platforms = self.define_platforms()
        self.creators_data = self.initialize_creators_data()
        self.market_data = self.initialize_market_data()
        
    def define_platforms(self):
        """Définit les plateformes et leurs caractéristiques"""
        return {
            'OnlyFans': {
                'color': '#00A2FF',
                'founded': 2016,
                'fees': 20,  # Pourcentage pris par la plateforme
                'content_type': 'Mixed',
                'monthly_users': 250000000,
                'creators_count': 3000000,
                'avg_creator_earnings': 180
            },
            'MyM': {
                'color': '#FF6B35',
                'founded': 2018,
                'fees': 20,
                'content_type': 'Adult',
                'monthly_users': 50000000,
                'creators_count': 500000,
                'avg_creator_earnings': 220
            },
            'Fansly': {
                'color': '#FF4081',
                'founded': 2020,
                'fees': 20,
                'content_type': 'Adult',
                'monthly_users': 100000000,
                'creators_count': 800000,
                'avg_creator_earnings': 190
            },
            'Patreon': {
                'color': '#FF9500',
                'founded': 2013,
                'fees': 5,
                'content_type': 'Mixed',
                'monthly_users': 80000000,
                'creators_count': 250000,
                'avg_creator_earnings': 150
            },
            'JustForFans': {
                'color': '#4CAF50',
                'founded': 2019,
                'fees': 20,
                'content_type': 'Adult',
                'monthly_users': 30000000,
                'creators_count': 200000,
                'avg_creator_earnings': 280
            },
            'LoyalFans': {
                'color': '#9C27B0',
                'founded': 2020,
                'fees': 15,
                'content_type': 'Adult',
                'monthly_users': 40000000,
                'creators_count': 300000,
                'avg_creator_earnings': 210
            }
        }
    
    def initialize_creators_data(self):
        """Initialise les données des créateurs"""
        categories = ['Fitness', 'Cosplay', 'Lifestyle', 'Adult', 'Gaming', 'Art', 'Music', 'Education']
        countries = ['USA', 'UK', 'Canada', 'Australia', 'Germany', 'France', 'Brazil', 'Japan']
        
        creators = []
        for i in range(100):
            platform = random.choice(list(self.platforms.keys()))
            category = random.choice(categories)
            country = random.choice(countries)
            
            # Revenus basés sur la plateforme et la catégorie
            base_earnings = self.platforms[platform]['avg_creator_earnings']
            if category == 'Adult':
                earnings_multiplier = random.uniform(1.5, 4.0)
            elif category == 'Fitness':
                earnings_multiplier = random.uniform(1.2, 2.5)
            else:
                earnings_multiplier = random.uniform(0.8, 2.0)
            
            monthly_earnings = base_earnings * earnings_multiplier
            followers = random.randint(1000, 500000)
            
            creators.append({
                'id': i + 1,
                'username': f'creator_{i+1}',
                'platform': platform,
                'category': category,
                'country': country,
                'monthly_earnings': monthly_earnings,
                'followers': followers,
                'subscription_price': random.randint(5, 50),
                'engagement_rate': random.uniform(2, 15),
                'content_quality': random.uniform(3, 5),
                'active_since': datetime.now() - timedelta(days=random.randint(30, 1000))
            })
        
        return pd.DataFrame(creators)
    
    def initialize_market_data(self):
        """Initialise les données de marché historiques"""
        dates = pd.date_range('2020-01-01', datetime.now(), freq='M')
        data = []
        
        for date in dates:
            for platform, info in self.platforms.items():
                # Croissance basée sur l'âge de la plateforme
                base_users = info['monthly_users']
                base_creators = info['creators_count']
                
                # Facteur de croissance
                months_since_founded = (date.year - info['founded']) * 12 + date.month
                growth_factor = min(months_since_founded * 0.1, 3.0)
                
                # Variations aléatoires réalistes
                user_variation = random.normalvariate(0, 0.05)
                creator_variation = random.normalvariate(0, 0.03)
                
                monthly_users = base_users * growth_factor * (1 + user_variation)
                creators_count = base_creators * growth_factor * (1 + creator_variation)
                revenue = creators_count * info['avg_creator_earnings'] * 0.2  # 20% de frais
                
                data.append({
                    'date': date,
                    'platform': platform,
                    'monthly_users': monthly_users,
                    'creators_count': creators_count,
                    'revenue_millions': revenue / 1000000,
                    'market_share': 0  # À calculer plus tard
                })
        
        df = pd.DataFrame(data)
        
        # Calcul de la part de marché
        for date in df['date'].unique():
            date_data = df[df['date'] == date]
            total_revenue = date_data['revenue_millions'].sum()
            df.loc[df['date'] == date, 'market_share'] = (
                df[df['date'] == date]['revenue_millions'] / total_revenue * 100
            )
        
        return df
    
    def update_live_data(self):
        """Met à jour les données en temps réel"""
        # Mise à jour aléatoire des revenus des créateurs
        for idx in self.creators_data.index:
            variation = random.normalvariate(0, 0.1)
            self.creators_data.loc[idx, 'monthly_earnings'] *= (1 + variation)
            self.creators_data.loc[idx, 'followers'] += random.randint(-50, 100)
            self.creators_data.loc[idx, 'engagement_rate'] += random.uniform(-0.5, 0.5)
            self.creators_data.loc[idx, 'engagement_rate'] = max(0, min(20, self.creators_data.loc[idx, 'engagement_rate']))
    
    def display_header(self):
        """Affiche l'en-tête du dashboard"""
        st.markdown('<h1 class="main-header">💎 Analyse des Plateformes de Contenu Adulte - Live</h1>', 
                   unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="live-badge">🔴 DONNÉES EN TEMPS RÉEL - MISES À JOUR CONTINUES</div>', 
                       unsafe_allow_html=True)
            st.markdown("**Analyse en direct du marché des plateformes de contenu adulte et créateurs**")
        
        current_time = datetime.now().strftime('%H:%M:%S')
        st.sidebar.markdown(f"**🕐 Dernière mise à jour: {current_time}**")
    
    def display_market_overview(self):
        """Affiche la vue d'ensemble du marché"""
        st.markdown('<h3 class="section-header">📊 VUE D\'ENSEMBLE DU MARCHÉ</h3>', 
                   unsafe_allow_html=True)
        
        # Calcul des métriques globales
        total_revenue = self.market_data.groupby('platform')['revenue_millions'].last().sum()
        total_creators = sum([info['creators_count'] for info in self.platforms.values()])
        total_users = sum([info['monthly_users'] for info in self.platforms.values()])
        avg_earnings = self.creators_data['monthly_earnings'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Revenus Mensuels Totaux",
                f"${total_revenue:.0f}M",
                "+12.5% vs mois dernier"
            )
        
        with col2:
            st.metric(
                "Créateurs Actifs",
                f"{total_creators:,}",
                "+8.3% vs mois dernier"
            )
        
        with col3:
            st.metric(
                "Utilisateurs Mensuels",
                f"{total_users:,}",
                "+15.2% vs mois dernier"
            )
        
        with col4:
            st.metric(
                "Revenu Moyen/Créateur",
                f"${avg_earnings:.0f}/mois",
                "+5.7% vs mois dernier"
            )
    
    def create_platform_comparison(self):
        """Crée la comparaison entre plateformes"""
        st.markdown('<h3 class="section-header">🏆 COMPARAISON DES PLATEFORMES</h3>', 
                   unsafe_allow_html=True)
        
        # Dernières données disponibles
        latest_data = self.market_data[self.market_data['date'] == self.market_data['date'].max()]
        
        tab1, tab2, tab3, tab4 = st.tabs(["Revenus & Part de Marché", "Utilisateurs", "Créateurs", "Performance Détail"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Graphique des parts de marché
                fig = px.pie(latest_data, 
                            values='market_share', 
                            names='platform',
                            title='Part de Marché par Plateforme',
                            color='platform',
                            color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenus par plateforme
                fig = px.bar(latest_data, 
                            x='platform', 
                            y='revenue_millions',
                            title='Revenus Mensuels par Plateforme (Millions $)',
                            color='platform',
                            color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                fig.update_layout(xaxis_title="", yaxis_title="Revenus ($ Millions)")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution des utilisateurs
                fig = px.line(self.market_data, 
                             x='date', 
                             y='monthly_users',
                             color='platform',
                             title='Évolution des Utilisateurs Mensuels',
                             color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Utilisateurs actuels
                fig = px.bar(latest_data, 
                            x='platform', 
                            y='monthly_users',
                            title='Utilisateurs Mensuels Actuels',
                            color='platform',
                            color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                fig.update_layout(xaxis_title="", yaxis_title="Utilisateurs")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Évolution des créateurs
                fig = px.line(self.market_data, 
                             x='date', 
                             y='creators_count',
                             color='platform',
                             title='Évolution du Nombre de Créateurs',
                             color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Créateurs actuels
                fig = px.bar(latest_data, 
                            x='platform', 
                            y='creators_count',
                            title='Nombre de Créateurs Actuels',
                            color='platform',
                            color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                fig.update_layout(xaxis_title="", yaxis_title="Créateurs")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Tableau détaillé des performances
            platform_stats = []
            for platform, info in self.platforms.items():
                platform_data = latest_data[latest_data['platform'] == platform].iloc[0]
                creator_data = self.creators_data[self.creators_data['platform'] == platform]
                
                platform_stats.append({
                    'Plateforme': platform,
                    'Année de Lancement': info['founded'],
                    'Frais (%)': info['fees'],
                    'Type de Contenu': info['content_type'],
                    'Utilisateurs': f"{platform_data['monthly_users']:,.0f}",
                    'Créateurs': f"{platform_data['creators_count']:,.0f}",
                    'Revenus Mensuels': f"${platform_data['revenue_millions']:.1f}M",
                    'Part de Marché': f"{platform_data['market_share']:.1f}%",
                    'Revenu Moyen Créateur': f"${creator_data['monthly_earnings'].mean():.0f}"
                })
            
            st.dataframe(pd.DataFrame(platform_stats), use_container_width=True)
    
    def create_creators_analysis(self):
        """Analyse des créateurs et de leurs performances"""
        st.markdown('<h3 class="section-header">👑 ANALYSE DES CRÉATEURS</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["Top Performers", "Analyse par Catégorie", "Géographie", "Corrélations"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Top 10 créateurs par revenus
                top_earners = self.creators_data.nlargest(10, 'monthly_earnings')
                fig = px.bar(top_earners, 
                            x='username', 
                            y='monthly_earnings',
                            color='platform',
                            title='Top 10 Créateurs par Revenus Mensuels',
                            color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                fig.update_layout(xaxis_title="Créateur", yaxis_title="Revenus Mensuels ($)")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Distribution des revenus
                fig = px.histogram(self.creators_data, 
                                  x='monthly_earnings',
                                  nbins=50,
                                  title='Distribution des Revenus des Créateurs',
                                  color_discrete_sequence=['#FF416C'])
                fig.update_layout(xaxis_title="Revenus Mensuels ($)", yaxis_title="Nombre de Créateurs")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                # Revenus moyens par catégorie
                category_earnings = self.creators_data.groupby('category')['monthly_earnings'].mean().reset_index()
                fig = px.bar(category_earnings, 
                            x='category', 
                            y='monthly_earnings',
                            title='Revenus Moyens par Catégorie de Contenu',
                            color='category')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Nombre de créateurs par catégorie
                category_counts = self.creators_data['category'].value_counts().reset_index()
                category_counts.columns = ['category', 'count']
                fig = px.pie(category_counts, 
                            values='count', 
                            names='category',
                            title='Répartition des Créateurs par Catégorie')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Répartition géographique
                country_counts = self.creators_data['country'].value_counts().reset_index()
                country_counts.columns = ['country', 'count']
                
                # Carte choroplèthe simplifiée
                fig = px.choropleth(country_counts,
                                   locations='country',
                                   locationmode='country names',
                                   color='count',
                                   title='Répartition Géographique des Créateurs',
                                   color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Revenus moyens par pays
                country_earnings = self.creators_data.groupby('country')['monthly_earnings'].mean().reset_index()
                fig = px.bar(country_earnings, 
                            x='country', 
                            y='monthly_earnings',
                            title='Revenus Moyens par Pays',
                            color='monthly_earnings',
                            color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
        
        with tab4:
            # Analyse des corrélations
            corr_data = self.creators_data[['monthly_earnings', 'followers', 'engagement_rate', 'content_quality', 'subscription_price']]
            corr_matrix = corr_data.corr()
            
            fig = px.imshow(corr_matrix,
                           title='Corrélations entre les Métriques de Performance',
                           color_continuous_scale='RdBu_r',
                           aspect='auto')
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights sur les corrélations
            st.markdown("""
            **📈 Insights des Corrélations:**
            - Engagement vs Revenus: Relation positive forte
            - Followers vs Revenus: Relation modérée
            - Qualité du Contenu vs Engagement: Relation positive
            - Prix d'Abonnement vs Revenus: Relation complexe
            """)
    
    def create_growth_analysis(self):
        """Analyse de la croissance et des tendances"""
        st.markdown('<h3 class="section-header">📈 ANALYSE DE CROISSANCE</h3>', 
                   unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["Tendances Temporelles", "Projections", "Analyse Saisonnière"])
        
        with tab1:
            col1, col2 = st.columns(2)
            
            with col1:
                # Croissance cumulée des revenus
                platform_growth = self.market_data.pivot_table(
                    index='date', 
                    columns='platform', 
                    values='revenue_millions'
                ).cumsum()
                
                fig = px.line(platform_growth.reset_index().melt(id_vars=['date'], 
                                                               value_name='revenue_cumulative', 
                                                               var_name='platform'),
                             x='date', 
                             y='revenue_cumulative',
                             color='platform',
                             title='Croissance Cumulative des Revenus par Plateforme',
                             color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Taux de croissance mensuel
                monthly_growth = self.market_data.pivot_table(
                    index='date', 
                    columns='platform', 
                    values='revenue_millions'
                ).pct_change() * 100
                
                fig = px.line(monthly_growth.reset_index().melt(id_vars=['date'], 
                                                              value_name='growth_rate', 
                                                              var_name='platform'),
                             x='date', 
                             y='growth_rate',
                             color='platform',
                             title='Taux de Croissance Mensuel des Revenus (%)',
                             color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Projections basées sur les tendances historiques
            st.subheader("Projections 2024-2025")
            
            # Simulation de projections
            future_dates = pd.date_range(start=self.market_data['date'].max() + timedelta(days=30), 
                                       periods=12, freq='M')
            
            projection_data = []
            for platform, info in self.platforms.items():
                current_data = self.market_data[self.market_data['platform'] == platform].iloc[-1]
                base_revenue = current_data['revenue_millions']
                base_users = current_data['monthly_users']
                base_creators = current_data['creators_count']
                
                # Facteurs de croissance basés sur l'historique
                growth_rate = random.uniform(0.02, 0.08)  # 2-8% de croissance mensuelle
                
                for i, date in enumerate(future_dates):
                    growth_factor = (1 + growth_rate) ** (i + 1)
                    projection_data.append({
                        'date': date,
                        'platform': platform,
                        'revenue_millions': base_revenue * growth_factor,
                        'monthly_users': base_users * growth_factor,
                        'creators_count': base_creators * growth_factor,
                        'type': 'Projection'
                    })
            
            df_projection = pd.DataFrame(projection_data)
            
            # Combiner données historiques et projections
            historical = self.market_data.copy()
            historical['type'] = 'Historique'
            combined_data = pd.concat([historical, df_projection])
            
            fig = px.line(combined_data, 
                         x='date', 
                         y='revenue_millions',
                         color='platform',
                         line_dash='type',
                         title='Projection des Revenus 2024-2025',
                         color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # Analyse saisonnière
            self.market_data['month'] = self.market_data['date'].dt.month
            self.market_data['year'] = self.market_data['date'].dt.year
            
            seasonal_data = self.market_data.groupby(['platform', 'month'])['revenue_millions'].mean().reset_index()
            
            fig = px.line(seasonal_data, 
                         x='month', 
                         y='revenue_millions',
                         color='platform',
                         title='Saisonnalité des Revenus (Moyenne Mensuelle)',
                         color_discrete_map={p: info['color'] for p, info in self.platforms.items()})
            fig.update_xaxes(tickvals=list(range(1, 13)), 
                           ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **🎯 Insights Saisonniers:**
            - Pic en Janvier (résolutions du nouvel an)
            - Augmentation en été (vacances)
            - Baisse en Décembre (fêtes)
            """)
    
    def create_risk_analysis(self):
        """Analyse des risques et de la régulation"""
        st.markdown('<h3 class="section-header">⚠️ ANALYSE DES RISQUES</h3>', 
                   unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risques par plateforme
            risk_data = []
            for platform, info in self.platforms.items():
                risks = {
                    'Réglementaire': random.uniform(0.3, 0.9),
                    'Concurrentiel': random.uniform(0.2, 0.8),
                    'Technologique': random.uniform(0.1, 0.6),
                    'Réputation': random.uniform(0.4, 0.9),
                    'Dépendance Créateurs': random.uniform(0.3, 0.8)
                }
                for risk_type, score in risks.items():
                    risk_data.append({
                        'Plateforme': platform,
                        'Type de Risque': risk_type,
                        'Score': score
                    })
            
            df_risk = pd.DataFrame(risk_data)
            
            fig = px.bar(df_risk, 
                        x='Plateforme', 
                        y='Score',
                        color='Type de Risque',
                        title='Analyse des Risques par Plateforme',
                        barmode='group')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Facteurs d'impact réglementaire
            regulation_factors = {
                'Conformité Légale': 0.85,
                'Paiements & Banques': 0.78,
                'Protection Données': 0.72,
                'Contenu Illégal': 0.91,
                'Fiscalité': 0.65,
                'Droits Auteurs': 0.58
            }
            
            fig = px.bar(x=list(regulation_factors.values()), 
                        y=list(regulation_factors.keys()),
                        orientation='h',
                        title='Facteurs d\'Impact Réglementaire',
                        color=list(regulation_factors.values()),
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
    
    def create_sidebar(self):
        """Crée la sidebar avec les contrôles"""
        st.sidebar.markdown("## 🎛️ CONTRÔLES D'ANALYSE")
        
        # Filtres
        st.sidebar.markdown("### 🔍 Filtres")
        selected_platforms = st.sidebar.multiselect(
            "Plateformes à afficher:",
            list(self.platforms.keys()),
            default=list(self.platforms.keys())[:3]
        )
        
        selected_categories = st.sidebar.multiselect(
            "Catégories de contenu:",
            list(self.creators_data['category'].unique()),
            default=list(self.creators_data['category'].unique())
        )
        
        earnings_range = st.sidebar.slider(
            "Fourchette de revenus ($):",
            min_value=0,
            max_value=int(self.creators_data['monthly_earnings'].max()),
            value=(0, int(self.creators_data['monthly_earnings'].max()))
        )
        
        # Options d'affichage
        st.sidebar.markdown("### ⚙️ Options")
        auto_refresh = st.sidebar.checkbox("Rafraîchissement automatique", value=True)
        show_projections = st.sidebar.checkbox("Afficher les projections", value=True)
        
        # Bouton de rafraîchissement manuel
        if st.sidebar.button("🔄 Rafraîchir les données"):
            self.update_live_data()
            st.rerun()
        
        return {
            'selected_platforms': selected_platforms,
            'selected_categories': selected_categories,
            'earnings_range': earnings_range,
            'auto_refresh': auto_refresh,
            'show_projections': show_projections
        }

    def run_dashboard(self):
        """Exécute le dashboard complet"""
        # Mise à jour des données live
        self.update_live_data()
        
        # Sidebar
        controls = self.create_sidebar()
        
        # Header
        self.display_header()
        
        # Vue d'ensemble
        self.display_market_overview()
        
        # Navigation par onglets
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏆 Plateformes", 
            "👑 Créateurs", 
            "📈 Croissance", 
            "⚠️ Risques", 
            "💡 Insights",
            "ℹ️ À Propos"
        ])
        
        with tab1:
            self.create_platform_comparison()
        
        with tab2:
            self.create_creators_analysis()
        
        with tab3:
            self.create_growth_analysis()
        
        with tab4:
            self.create_risk_analysis()
        
        with tab5:
            st.markdown("## 💡 INSIGHTS STRATÉGIQUES")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🎯 Opportunités de Marché
                
                **🌍 Expansion Internationale:**
                - Marchés émergents: Amérique Latine, Asie du Sud-Est
                - Localisation du contenu nécessaire
                - Partenariats avec des créateurs locaux
                
                **📱 Innovation Technologique:**
                - Intégration IA pour recommandations
                - Expériences de réalité virtuelle
                - Outils analytics avancés pour créateurs
                
                **💼 Nouveaux Modèles:**
                - Contenu éducatif premium
                - Expériences de groupe
                - Abonnements à plusieurs niveaux
                """)
            
            with col2:
                st.markdown("""
                ### 🚨 Défis et Risques
                
                **⚖️ Réglementation:**
                - Lois en évolution rapide
                - Restrictions des processeurs de paiement
                - Conformité internationale complexe
                
                **🔐 Sécurité:**
                - Protection des données des créateurs
                - Lutte contre le contenu non autorisé
                - Sécurisation des transactions
                
                **💸 Viabilité Économique:**
                - Dépendance aux top créateurs
                - Concurrence sur les frais
                - Coûts technologiques croissants
                """)
            
            st.markdown("""
            ### 📊 Recommandations Stratégiques
            
            1. **Diversification du Contenu:** Élargir au-delà du contenu adulte traditionnel
            2. **Support Créateurs:** Programmes de formation et outils analytics
            3. **Innovation Technologique:** Investir dans l'IA et l'expérience utilisateur
            4. **Expansion Mondiale:** Stratégies de localisation adaptées
            5. **Conformité Proactive:** Anticiper les changements réglementaires
            """)
        
        with tab6:
            st.markdown("## 📊 À propos de ce dashboard")
            st.markdown("""
            Ce dashboard présente une analyse en temps réel du marché des plateformes de contenu adulte 
            et de leurs créateurs.
            
            **Méthodologie :**
            - Données basées sur des analyses de marché et modèles prédictifs
            - Mises à jour quotidiennes avec variations réalistes
            - Analyse multidimensionnelle (revenus, croissance, risques)
            
            **Plateformes suivies :**
            - OnlyFans, MyM, Fansly, Patreon, JustForFans, LoyalFans
            - Analyse comparative des performances
            - Focus sur les dynamiques de croissance
            
            **⚠️ Note :** Les données sont simulées pour la démonstration. 
            Dans un contexte réel, elles proviendraient de sources officielles et d'analyses de marché.
            
            **🔒 Confidentialité:** Toutes les données des créateurs sont anonymisées et agrégées.
            """)
        
        # Rafraîchissement automatique
        if controls['auto_refresh']:
            time.sleep(30)  # Rafraîchissement toutes les 30 secondes
            st.rerun()

# Lancement du dashboard
if __name__ == "__main__":
    dashboard = AdultPlatformsDashboard()
    dashboard.run_dashboard()