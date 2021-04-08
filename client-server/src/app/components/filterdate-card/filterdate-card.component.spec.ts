import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterdateCardComponent } from './filterdate-card.component';

describe('FilterdateCardComponent', () => {
  let component: FilterdateCardComponent;
  let fixture: ComponentFixture<FilterdateCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FilterdateCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FilterdateCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
