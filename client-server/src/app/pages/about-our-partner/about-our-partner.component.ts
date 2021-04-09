import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-about-our-partner',
  templateUrl: './about-our-partner.component.html',
  styleUrls: ['./about-our-partner.component.scss']
})
export class AboutOurPartnerComponent implements OnInit {

  constructor(
    private titleService: Title,
  ) { }

  ngOnInit(): void {
    this.titleService.setTitle("About Our Partner | Find Dining Scarborough");
  }

}
