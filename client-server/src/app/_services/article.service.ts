import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const ARTICLE_API = AUTH_API + '/article/all/'

@Injectable({
  providedIn: 'root'
})
export class ArticleService {

  constructor(private http: HttpClient) { }

  getArticles(): Observable<any> {
    const endpoint = ARTICLE_API;
    return this.http.get(endpoint);
  }

}
