import streamlit as st



# What resources will a user have : 

# storeage
# Memory 

# use per day 
# 4 hours storge 
# 8 Hours storge 
# 16 Hours  storge


# Server Specification 
# Storage 500GB
# Memory 16GB 



### Function Area 


# total Average Storage per day = [Number of Users] * [Storage for 1 User per day]
def total_average_storage_per_day(Number_of_Users):
	return int(Number_of_Users) * 5

# total Storage per 4 hours =  [Number of Users] * [Storage for 1 User per day] * 4
def total_storage_per_fourhours(Number_of_Users, storage_user):
	return int(Number_of_Users) * int(storage_user) * 4

# total Storage per 8 hours =  [Number of Users] * [Storage for 1 User per day] * 8
def total_storage_per_eighthours(Number_of_Users, storage_user):
	return int(Number_of_Users) * int(storage_user) * 8

# total Storage per 4 hours =  [Number of Users] * [Storage for 1 User per day] * 16
def total_storage_per_sixteenhours(Number_of_Users, storage_user):
	return int(Number_of_Users) * int(storage_user) * 16

# total total Memory = [Number of Users] * [Memory  for 1 User per day]
def total_memory_per_day(Number_of_Users, memory_user):
	return int(Number_of_Users) * int(memory_user)

# number of servers 
# number of servers = [Total USER Storage  ]/ [Total Server Storage ]
# number of servers = [Total User Memory ]/ [Total Memory]

numberofuser = st.text_input("Number of Users", value="1", max_chars=None)
storage_per_user = st.text_input("Storage per Users", value="1", max_chars=None)

storage_per_user_4hrs = st.text_input("4Hr Storage per Users", value="1", max_chars=None)
storage_per_user_8hrs = st.text_input("8Hr Storage per Users", value="1", max_chars=None)
storage_per_user_16hrs = st.text_input("16Hr Storage per Users", value="1", max_chars=None)

memory_per_user = st.text_input("Memory per Users", value="1", max_chars=None)

st.write("Total Average per Day : " + str(total_average_storage_per_day(numberofuser)))
st.write("Total Storage for User per 4Hr : " + str(total_storage_per_fourhours(numberofuser, storage_per_user_4hrs)))
st.write("Total Storage for User per 8Hr : " + str(total_storage_per_eighthours(numberofuser, storage_per_user_8hrs)))
st.write("Total Storage for User per 16Hr : " + str(total_storage_per_sixteenhours(numberofuser, storage_per_user_16hrs)))
st.write("Total Memory per Day : " + str(total_memory_per_day(numberofuser, memory_per_user)))


### End of Funcation area