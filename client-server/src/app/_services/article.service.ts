import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const AUTH_API = '/api';
const ARTICLE_API = AUTH_API + '/article/all/'

@Injectable({
  providedIn: 'root'
})
export class ArticleService {

  articleTitle: string = "";
  articleModifiedDate: string = "";
  articleContentString: string = "";

  constructor(private http: HttpClient) { }

  /*
  @Input: None
  @Output: List of article objects available to the user based
          on their role
  Retrieves all the viewable articles a user is allowed to see
  */
  getArticles(): Observable<any> {
    const endpoint = ARTICLE_API;
    return this.http.get(endpoint);
  }

  /*
  @Input: The article to open
  @Output: None
  Sets the htmlString to the content of the article to be opened
  */
  openArticle(article): void {
    this.articleTitle = article.title;
    this.articleModifiedDate = article.modified_at;
    this.articleContentString = article.content;
  }

}
