from django.shortcuts import render
import requests, html5lib, time
from bs4 import BeautifulSoup
from .models import Search
value,count,ppagecount = (0,0,0)

def index(request):
    recent_search = Search.objects.all()
    return render(request,'scrapEngine/index.html',{'recent_search':recent_search})

def jobs(request):
    if request.method == 'POST':
        query = request.POST['query']
        paginator = request.POST['paginator']
        try:
            q = Search.objects.get(recent_search=query) 
            if q:
                pass
        except:
             Search.objects.create(recent_search=query)
        final_query = '+'.join(query.split(' '))
        url = 'https://in.indeed.com/jobs?q=' + final_query + paginator
        
        target = requests.get(url).text
        soup = BeautifulSoup(target,'html5lib')
        l = list()
        global value
        page = int(value/10) + 1
        
        for imp in soup.find_all('div', class_='jobsearch-SerpJobCard'):
            try:
                j_id = imp['data-jk']
                title = imp.h2.a.text.strip()
                company = imp.div.div.span.text.strip()
                location = imp.div.find('span', class_='location').text.strip()
                salary = imp.find('div', class_='salarySnippet').text.strip()
                global count
                count+=1
                global ppagecount
                ppagecount+=1

            except:
                continue

            jobs = {'url':url,'id':j_id,'title':title,'company':company,'location':location,'salary':salary}
            l.append(jobs) 

        if count != 0:
            value += 10
            paginator = '&start=' + str(value)
        
        context = {'jobs':l,'paginator':paginator, 'query':query, 'value':value%10 + 1}

        return render(request,'scrapEngine/index.html',context)

def job_detail(request):
    return render(request,'scrapEngine/detail.html')
