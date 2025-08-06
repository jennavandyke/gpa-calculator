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
	gpa = round(gpa, 5)
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
