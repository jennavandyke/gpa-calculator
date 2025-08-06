# GETTING THE DATA FILE ======================================================

import csv
import os
from tabulate import tabulate
from google.colab import files

is_using_example = True # By default

# Ask user if they want to use the example file or submit their own
print()
while True:
  file_input = input("Do you want to submit your own file or use the example? Enter 'o' for your own file or 'e' for the example. ")
	
	# User enters their own file
  if file_input == 'o':
    print()
    is_using_example = False
    print('''You can use Google Sheets to organize your data. Make sure your file has the same formatting as the file at this link or the program will NOT work: https://shorturl.at/ncSmS
Download your data as a .csv file and upload it below.''')
      
    uploaded = files.upload()  # This opens a file upload dialog

    # Get the filename from the uploaded file dictionary
    if uploaded:
      user_file = list(uploaded.keys())[0]
      try:
        with open(user_file, mode='r', newline='') as file:
          data = list(csv.reader(file))
          break
      except Exception as e:
        print("An error occurred while reading the file:", e)
        raise e
        continue
    else:
      print("No file uploaded. Exiting.")
      exit()

	# User wants to use the example file
  elif file_input == 'e':
	  with open('sample_data.csv', mode='r',newline='') as file:
		  data = list(csv.reader(file))
	  break
		
	# Invalid input
  else:
	  print("That's not a valid response.")
	  continue


# PREPARING FILE FOR GPA CALCULATION ========================================

# First, let's delete all of the lower-division coursework since that doesn't count toward upper-div GPA.

# Identifying lower-division columns
row_1 = data[0]
columns_to_remove = []
for i in range(len(row_1)):
	if i < 3: # Skipping perm, name, and GPA columns
		continue
	else:
		coursenum_length = len(row_1[i])
		if coursenum_length < 3: # Upper-div course numbers are 3+ numbers long
			columns_to_remove.append(i)

# Removing lower-division columns
fresh_data = [[item for column, item in enumerate(data_row) if column not in columns_to_remove] for data_row in data]
data = fresh_data.copy() # Because I still want to call it 'data'

# Print the data in a table so the user can see the letter grades we are starting with.
print()
while True:
	if is_using_example:
		display = input("Would you like to view each student's upper-division grades? Enter 'y' or 'n': ")
	else:
		display = input("Would you like to view each student's upper-division grades? Keep in mind that if your spreadsheet includes a large number of students, the tabular format cannot fully display. Enter 'y' or 'n': ")

	if display == 'y':
		transpose = list(map(list,zip(*data)))
		headers = transpose[0]
		rows = transpose[1:]
		table_data = tabulate(rows,headers=headers,tablefmt='grid')
		print('''
UPPER-DIVISION DATA:
''' + str(table_data))
		print()
		break
	elif display =='n':
		break
	else:
		print("That's not a valid input.")
		continue

# We're going to need to start keeping track of the number of total units taken by each student
import numpy as np
total_units = np.zeros(len(data))

# Now let's prepare to convert the letter grades into grade points.
codes_to_check = ['P','NP','NG','I','W','IP','S','U','NC']
grades_dic = {
'A+': '4.0',
'A-': '3.7',
'A': '4.0',
'B+': '3.3',
'B-': '2.7',
'B': '3.0',
'C+': '2.3',
'C-': '1.7',
'C': '2.0',
'D+': '1.3',
'D-': '0.7',
'D': '1.0',
'F': '0.0'
}

# These courses need special attention, because students can choose to take them for however many units they want.
ind_to_check_units = []
courses_to_check = ['150','198','199']
for i in range(len(data[0])):
	for course in courses_to_check:
		if data[0][i] == course:
			ind_to_check_units.append(i)


# CONVERTING LETTER GRADES TO GRADE POINTS

if is_using_example: # Manually assigning number of units for these classes
	# Einstein:
	data[1][32] = float(4.0 * 4.0)
	data[1][33] = float(4.0 * 4.0)
	data[1][36] = float(4.0 * 4.0)
	data[1][37] = float(4.0 * 4.0)
	data[1][38] = float(4.0 * 4.0)
	total_units[1] += 20
	# Feynman:
	data[3][32] = float(3.0 * 4.0)
	data[3][33] = float(4.0 * 4.0)
	data[3][35] = float(3.0 * 2.0)
	data[3][36] = float(4.0 * 3.0)
	data[3][37] = float(3.7 * 4.0)
	total_units[3] += 17
else:
	pass # Will do this inside loop


# Now we are ready to fix the rest of the data in a loop
for i in range(1,len(data)):
	for j in range(len(data[i])):
		data_item = str(data[i][j])
		
		# First, keep only the most recent grade
		try:
			slash_ind = data_item.index('/')
			data_item = data_item[slash_ind+1:]
		except ValueError:
			pass

		# Now, make all P, NP, NG, I, W, IP, S, U, NC grade codes blank
		for code in codes_to_check:
			if data_item == code:
				data_item = ''
				break
		
		# Now, translate all letter grades to grade points
		if j not in ind_to_check_units: # Excluding 150, 198, and 199
			if data_item in grades_dic:
				data_item = float(grades_dic[data_item]) * 4.0 # Multiply by 4 units to get grade points
				total_units[i] += 4
		else: # For 150, 198, and 199
			if is_using_example:
				pass # Already did this outside loop
			else:
				if data[i][j] != '':
					while True:
						num_units = input("For " + data[i][1] + ", how many units did they take " + data[0][j] + " for? ")
						try:
							num_units = float(num_units)
							break
						except ValueError:
							print("That's not a number!")
							continue
					data_item = float(grades_dic[data_item]) * num_units
					total_units[i] += num_units

		data[i][j] = (data_item)


# GPA CALCULATION ===============================================

# So far, we have the number of grade points earned in each class, and the total number of units. We simply have to sum the grade points earned, and then divide this by the units, and we have the GPA!

# First, make sure that we have all float values and no strings.

for i in range(1,len(data)):
	for j in range(3,len(data[i])):
		if data[i][j] != '':
			data[i][j] = float(data[i][j])

# We are also going to want to assign students' honors status, so let's create an empty list of that now.
honors_list = [""] * len(data)
honors_list[0] = "Honors Status"

# Now, loop through and calculate each student's GPA, and assign it to the proper slot in the data list
for i in range(1,len(data)):
	total_gp = 0 # Grade points
	for j in range(3,len(data[i])):
		if data[i][j] != '':
			total_gp += data[i][j]
	
	# Calculate and assign gpa
	gpa = total_gp / total_units[i]
	gpa = round(gpa, 3)
	data[i][2] = gpa

	# Assign honors status
	if gpa >= 3.8:
		honors_list[i] = "Highest Honors"
	elif gpa >= 3.5 and gpa < 3.8:
		honors_list[i] = "Honors"
	else:
		honors_list[i] = ""


# GPA OUTPUT ========================================================

print()

# Make printable data
data_toprint = [sublist[:3] for sublist in data]
for i in range(len(honors_list)):
	data_toprint[i].append(honors_list[i])

# First, in alphabetical order
while True:
	alpha = input("Would you like to view the students' GPAs in alphabetical order? Enter 'y' or 'n': ")
	if alpha == 'y':
		# First, alphabetize
		header = data_toprint[0]	
		data_toprint = sorted(data_toprint[1:], key=lambda x: x[1])
		data_toprint = [header] + data_toprint	

		# Now, make into table
		transpose = list(map(list,zip(*data_toprint)))
		headers = transpose[0]
		rows = transpose[1:]
		table_data = tabulate(rows,headers=headers,tablefmt='grid')
		print('''
ALPHABETICAL ORDER:
''' + str(table_data))

		# Asking the user if they would like a download of alphabetical data
		print()
		while True:
			downloading = input("Would you like to download this data in a .csv file? It will be under the name 'alphabetical_data.csv'. Enter 'y' or 'n': ")
			if downloading == 'y':
				with open('alphabetical_data.csv','w',newline='') as file:
					writer = csv.writer(file)
					writer.writerows(data_toprint)
				files.download('alphabetical_data.csv')
				break
			elif downloading == 'n':
				break
			else:
				print("That's not a valid input.")
				continue

		break

	elif alpha == 'n':
		break
	else:
		print("That's not a valid input.")
		continue

# Second, in order of GPA

print()
while True:
    gpa_order = input("Would you like to view the students' GPAs in order of highest to lowest? Enter 'y' or 'n': ")
    if gpa_order == 'y':
        # First, order the data
        header = data_toprint[0]
        data_toprint = sorted(data_toprint[1:], key=lambda x: x[2],reverse=True)
        data_toprint = [header] + data_toprint

        # Now, make into table
        transpose = list(map(list,zip(*data_toprint)))
        headers = transpose[0]
        rows = transpose[1:]
        table_data = tabulate(rows,headers=headers,tablefmt='grid')
        print('''
HIGHEST TO LOWEST GPA:
''' + str(table_data))

        # Asking the user if they would like a download of highest-to-lowest data
        print()
        while True:
            downloading = input("Would you like to download this data in a .csv file? It will be under the name 'hightolow_data.csv'. Enter 'y' or 'n': ")
            if downloading == 'y':
                with open('hightolow_data.csv','w',newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data_toprint)
                files.download('hightolow_data.csv')
                break
            elif downloading == 'n':
                break
            else:
                print("That's not a valid input.")
                continue

        break

    elif gpa_order == 'n':
        break
    else:
        print("That's not a valid input.")
        continue
