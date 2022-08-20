import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.title('CSV Reader')
file = st.sidebar.file_uploader('Upload a CSV', type="csv")
if file:
	df = pd.read_csv(file)
	tab1, tab2, tab3 = st.tabs(["DataFrame","Pclass","Survived"])
	with tab1:
		st.header("DataFrame")
		st.subheader("First two lines from the DataFrame")
		first_lines=df.head(2)
		st.dataframe(first_lines)
		with st.expander("See here the complete DataFrame"):
			st.dataframe(df)
	# st.markdown("---")

	with tab2:
		fig1 = plt.figure(figsize=(10,4))
		sns.countplot(x='Pclass',data=df)

		st.pyplot(fig1)

	# fig2 = plt.figure(figsize=(10,4))
	# sns.countplot(x='Sex',data=df)

	# st.pyplot(fig2)

		fig3 = plt.figure(figsize=(10,4))
		sns.boxplot(x='Pclass',
					y='Age',
					data=df)

		st.pyplot(fig3)

	with tab3:
		st.header("Survived")
		
		fig4 = plt.figure(figsize=(10,4))
		sns.countplot(x='Survived',data=df.loc[df['Sex']=='male'])
		fig5 = plt.figure(figsize=(10,4))
		sns.countplot(x='Survived',data=df.loc[df['Sex']=='female'])
		
		fig6 = plt.figure(figsize=(10,4))
		sns.countplot(x='Pclass',
					data=df.loc[(df['Sex']=="female")&(df['Survived']==1)])
		fig7 = plt.figure(figsize=(10,4))
		sns.countplot(x='Pclass',
					data=df.loc[(df['Sex']=="male")&(df['Survived']==1)])

		st.subheader("[Men] Dead VS Survivors")
		st.pyplot(fig4)
		st.subheader("[Women] Dead VS Survivors")
		st.pyplot(fig5)
		st.subheader("Women survived by Pclass")
		st.pyplot(fig6)
		st.subheader("Men survived by Pclass")
		st.pyplot(fig7)