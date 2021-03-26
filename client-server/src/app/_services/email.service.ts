import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = '/api/'
const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({
  providedIn: 'root'
})
export class EmailService {

  constructor(private http: HttpClient) {
   }

  /*
  @Input: JSON object containing subject and content (can be html)
  @Output: JSON object with messages indicating whether email is successfully sent or not
  */
   sendEmail(emailData): Observable<any> {
    const endpoint = API_URL + 'email/send/'
    return this.http.post<any>(endpoint, emailData, httpOptions);
  }

}
