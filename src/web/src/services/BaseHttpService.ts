export enum Method{
    Get = "get",
    Post = "post",
    Put = "put",
    Delete = "delete",
    Head = "head"
}

export interface HttpServiceRequest<TResult>{
    url: string,
    method: Method,
    callback: (response:Response) => Promise<TResult>,
    init?: (requestInit: RequestInit) => void
}

export async function jsonCallback<TResult>(response:Response): Promise<TResult>{
    return (await response.json()) as TResult;
}

export async function rawCallback(response:Response): Promise<string>{
    return await response.text();
}

export async function customCallback<TResult>(response:Response, caster:(src:string) => TResult): Promise<TResult>{
    return caster(await response.text());
}

function bodyParser<T>(parameter:string|T, init:RequestInit){
    if(typeof parameter === "string"){
        init.body = parameter;
    }else{
        init.body = JSON.stringify(parameter);
        init.headers = {
            "Content-Type": "application/json"
        }
    }
}

export default class BaseHttpService{

    constructor(protected baseUrl:string){

    }

    protected async send<TResult>({url, method, callback, init}:HttpServiceRequest<TResult>):Promise<TResult>{
        return new Promise<TResult>((resolve, reject) => {
            const requestInit = {
                method: method.valueOf()
            };
            if(init){
                init(requestInit);
            }
            fetch(`${this.baseUrl}/${url}`, requestInit)
            .then(response => callback(response)
                .then(result => resolve(result))
                .catch(reject))
            .catch(reject)
        });
    }

    protected async get<TResult>(url:string):Promise<TResult>{
        return this.send<TResult>({
            url: url,
            callback: jsonCallback,
            method: Method.Get
        });
    }
    
    protected async getRaw(url:string):Promise<string>{
        return this.send({
            url: url,
            callback: rawCallback,
            method: Method.Get
        });
    }

    protected post<T, TResult>(url:string, parameter:string|T):Promise<TResult>{
        return this.send<TResult>({
            url: url,
            callback: jsonCallback,
            init: (init) => bodyParser(parameter, init),
            method: Method.Post
        });
    }

    protected put<T, TResult>(url:string, parameter:string|T):Promise<TResult>{
        return this.send<TResult>({
            url: url,
            callback: jsonCallback,
            init: (init) => bodyParser(parameter, init),
            method: Method.Put
        });
    }
    
    protected async delete<TResult>(url:string):Promise<TResult>{
        return this.send<TResult>({
            url: url,
            callback: jsonCallback,
            method: Method.Get
        });
    }

    protected listen(url:string):EventSource{
        return new EventSource(url);
    }
}