import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AboutOurPartnerComponent } from './about-our-partner.component';

describe('AboutOurPartnerComponent', () => {
  let component: AboutOurPartnerComponent;
  let fixture: ComponentFixture<AboutOurPartnerComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AboutOurPartnerComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AboutOurPartnerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
