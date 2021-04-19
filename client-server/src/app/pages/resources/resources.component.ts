import { Component, OnInit } from '@angular/core';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-resources',
  templateUrl: './resources.component.html',
  styleUrls: ['./resources.component.scss']
})
export class ResourcesComponent implements OnInit {

  constructor(
    private titleService: Title,
  ) { }

  // File names of .pdf files stored in the folder /assets/pdf/
  pdfsFromAssets = [
    'COVID-19_Tax_Information_Session_for_Restaurant_Ownersv2.pdf',
  ];

  ngOnInit(): void {
    this.titleService.setTitle("Resources | Find Dining Scarborough");
  }

}
