import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { faCheck } from '@fortawesome/free-solid-svg-icons';
import { Title } from '@angular/platform-browser';
//import {MatIconModule} from '@angular/material/icon';
@Component({
  selector: 'app-thankyou-page',
  templateUrl: './thankyou-page.component.html',
  styleUrls: ['./thankyou-page.component.scss']
})
export class ThankyouPageComponent implements OnInit {

  constructor(private router: Router, private titleService: Title,) {}
  faCheckIcon = faCheck;
  ngOnInit(): void {
    this.titleService.setTitle("Thank You | Find Dining Scarborough"); 
  }

}
