from django.shortcuts import render
import requests, html5lib, time,threading
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from bs4 import BeautifulSoup
from .models import Search
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
value,count,ppagecount = (0,0,0)

def index(request):
    recent_search = Search.objects.all()
    return render(request,'scrapEngine/index.html',{'recent_search':recent_search})

def jobs(request):
    if request.method == 'POST':
        query = request.POST['query']
        paginator = request.POST['paginator']
        try:
            location = "&l=" + request.POST['location']
            print(location)
        except Exception as e:
            print(e)
        # print(location)
        try:
            q = Search.objects.get(recent_search=query) 
            if q:
                pass
        except:
             Search.objects.create(recent_search=query)
        final_query = '+'.join(query.split(' '))
        try:
            url = 'https://in.indeed.com/jobs?q=' + final_query + paginator + location
        except:
            url = 'https://in.indeed.com/jobs?q=' + final_query + paginator

        print(url)
        
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
                loc = imp.div.find('span', class_='location').text.strip()
                salary = imp.find('div', class_='salarySnippet').text.strip()
                global count
                count+=1
                global ppagecount
                ppagecount+=1

            except:
                continue
            
            jobs = {'url':url,'id':j_id,'title':title,'company':company,'location':loc,'salary':salary}
            l.append(jobs)

            job_url = url + '&vjk=' + j_id

            message = f'''
                Job Title = {title}
                Company = {company}
                Location = {loc}
                Salary = {salary}
                '''
            subject = "Here's something you might be interested in !!"
            email_from = settings.EMAIL_HOST_USER
            rec = ['dhruvpatel.pydev@gmail.com',]

            start = salary.split(' ')[0][1:]
            con = int(''.join(start.split(',')))

            html_message = render_to_string('scrapEngine/mail_template.html',request=request,context = {'url':url,'id':j_id,'title':title,'company':company,'location':loc,'salary':salary,
            'image' : 'https://images.unsplash.com/photo-1513005862547-c6071dd39fa9?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw&#%3D&ixlib=rb-1.2.1&auto=format&fit=crop'})

            # message = EmailMessage(subject,html_message,email_from,rec)
            # message.content_subtype = 'html'
            # message.send()
            def mail():
                message = EmailMessage(subject,html_message,email_from,rec)
                message.content_subtype = 'html'
                message.send()

            # plain_message = strip_tags(html_message).strip()
            # print(plain_message)

            # t1 = threading.Thread(target=EmailMessage,args=[subject,html_message,email_from,rec],)

            t1 = threading.Thread(target=mail)

            if con >= 10000:
                print('reached here |')
                t1.start()

            else:
                pass

        if count != 0:
            value += 10
            paginator = '&start=' + str(value)
            try:
                location = '&l=' + location
            except:
                location = ''
        context = {'jobs':l,'location':location,'paginator':paginator, 'query':query, 'value':value%10 + 1}
        
        return render(request,'scrapEngine/index.html',context)

def job_detail(request):
    return render(request,'scrapEngine/detail.html')
