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

  /**
   * Sends an email to info@finddining.ca
   * 
   * @param emailData - JSON object containing:
   *                      subject (string),
   *                      content (string; plain text or html)
   * @returns JSON object with messages indicating whether email is successfully sent or not
   */
   sendEmail(emailData): Observable<any> {
    const endpoint = API_URL + 'email/send/'
    return this.http.post<any>(endpoint, emailData, httpOptions);
  }

}
