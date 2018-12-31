import re
import pandas

ranking_of_degree = {}

def degreeCombination(degreeObj):
	for deg in degreeObj:
		#deg.degree name
		#deg.degree_rank
		possible_combination = []
		degree_rank = deg.degree_rank
		degree_name = deg.degree
		degree_name = re.sub('\n', '', degree_name)
		degree_name = degree_name.strip()
		degree_name = degree_name.lower()
		degree_name = re.sub(r'[.]+', '', degree_name)
		degree_name = re.sub(r'[\(\[].*?[\)\]]', '', degree_name)

		if '-' in degree_name:
			degree_name = degree_name.split('-')
			for d in degree_name:
				if '/' in d:
					d = d.split('/')
					for i in d:
						possible_combination.append(i.strip())
				else:
					possible_combination.append(d.strip())
		else:
			possible_combination.append(degree_name.strip())

		try:
			ranking_of_degree[int(degree_rank)] = possible_combination
		except:
			pass
	return ranking_of_degree
