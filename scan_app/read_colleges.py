import re
import pandas

def clgCombination(collegeObj):
	ranking_of_college = {}
	for clg in collegeObj:
		possible_combinations = []
		clg.clg_name = clg.clg_name.lower()
		clg.clg_name = re.sub(r"\t+", " ", clg.clg_name)
		clg.clg_name = re.sub(r'\n', ' ', clg.clg_name)
		clg.clg_name = re.sub(r"\s+", " ", clg.clg_name)
		clg.clg_name = re.sub(r',', "", clg.clg_name)
		clg.clg_name = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', clg.clg_name)

		possible_combinations.append(clg.clg_name)
		#college short form without '&' and 'of'
		#if 'of' in clg.clg_name and '&' in clg.clg_name:
		try:
			college_short_name = ''
			college_short = clg.clg_name.split(' ')
			for word in college_short:
				if word == 'of':
					pass
				elif word == '&':
					pass
				else:
					college_short_name += word[0]
		except:
			college_short_name = clg.clg_name

		possible_combinations.append(college_short_name)

		#college short form with of
#		if 'of' in clg.clg_name:
		try:
			college_short_name_with_of = ''
			college_short = clg.clg_name.split(' ')
			for word in college_short:
				if word == '&' or word == 'and':
					pass
				else:
					college_short_name_with_of += word[0]
		except:
			college_short_name_with_of = clg.clg_name
		possible_combinations.append(college_short_name_with_of)

		#college short name with and
#		if '&' in clg.clg_name:
		try:
			college_short_name_with_and = ''
			college_short = clg.clg_name.split(' ')
			for word in college_short:
				if word == 'of':
					pass
				else:
					college_short_name_with_and += word[0]
		except:
			college_short_name_with_and = clg.clg_name
		possible_combinations.append(college_short_name_with_and)

		#college short with 'a' of and
		#college short with 'and' of and
		try:
			college_short_name_with_a_and = ''
			college_short_name_with_and_and = ''
			clg.clg_name_with_replaced_and = ''
			college_short = clg.clg_name.split(' ')
			for word in college_short:
				if word == '&':
					college_short_name_with_a_and += 'a'
					college_short_name_with_and_and += ' and '
					clg.clg_name_with_replaced_and += 'and '
				else:
					college_short_name_with_a_and += word[0]
					college_short_name_with_and_and += word[0]
					clg.clg_name_with_replaced_and += word + ' '
		except:
			college_short_name_with_a_and = clg.clg_name
		possible_combinations.append(college_short_name_with_a_and)
		possible_combinations.append(college_short_name_with_and_and)
		possible_combinations.append(clg.clg_name_with_replaced_and.strip())

		#college short name with 'and' and 'of'
		try:
			college_short_name_with_and_of = ''
			college_short = clg.clg_name.split(' ')
			for word in college_short:
				college_short_name_with_and_of += word[0]
		except:
			college_short_name_with_and_of = clg.clg_name
		possible_combinations.append(college_short_name_with_and_of)

		#college name with location
#		if 'indian institute of management' in clg.clg_name or 'indian institute of technology' in clg.clg_name:
		flag = 0
		try:
			college_short_name_iim_iit = ''
			if 'indian institute of management' in clg.clg_name:
				college_short = clg.clg_name.split(' ')
				college_short_name_iim_iit += 'iim ' + str(college_short[-1])
				flag = 1
			elif 'indian institute of technology' in clg.clg_name:
				college_short = clg.clg_name.split(' ')
				college_short_name_iim_iit += 'iit ' + str(college_short[-1])
				flag = 1
		except:
			college_short_name_iim_iit = clg.clg_name

		if flag == 1:
			possible_combinations.append(college_short_name_iim_iit)


		possible_combinations = list(set(possible_combinations))
		ranking_of_college[int(clg.clg_rank)] = possible_combinations
		#with open('college.txt','w') as s:
		#	s.write(str(ranking_of_college));
	return ranking_of_college
