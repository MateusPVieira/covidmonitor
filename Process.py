def get_newcases(cases, new):
  c = newcases = newcasesmedia = 0
  newst = []
  record = []
  for row in cases:
    record.append(row)
  for row in record:
    if c == 14:
      break
    if c == 0:
      newcases = int(row.totcasos)
    newst.append(row.totcasos)
  newst.insert(0, new['confirmados'])
  if len(newst) >= 15:
    for i in range(len(newst)):
      if i == 15:
        break
      newcasesmedia = newcasesmedia + (int(newst[i-1]) - int(newst[(i)]))
  else:
    processed = {'novoscasos': 0, 'novoscasosmedia': 0}
    return processed

  newcasesmedia = round((newcasesmedia/270)*100)
  newcases = new['confirmados'] - newcases
  processed = {'novoscasos': newcases, 'novoscasosmedia': newcasesmedia}
  return processed


def get_graph_data(db):
  dbrecord = {'datagraph': [], 'novoscasos': [], 'novoscasosmedia': [], 'uti' : []}
  record =[]
  for row in db: #limit 14
    record.append(row)
  for row in reversed(range(len(record))):

    dbrecord['datagraph'].append(record[row].datagraph)
    dbrecord['novoscasos'].append(record[row].newcases)
    dbrecord['novoscasosmedia'].append(record[row].newcasesmedia)
    dbrecord['uti'].append(record[row].uti)
  return dbrecord

  


  

