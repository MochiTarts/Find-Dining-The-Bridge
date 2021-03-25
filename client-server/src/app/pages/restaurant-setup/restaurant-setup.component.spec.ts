<<<<<<< HEAD:client-server/src/app/pages/restaurant-setup/restaurant-setup.component.spec.ts
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RestaurantSetupComponent } from './restaurant-setup.component';

describe('RestaurantSetupComponent', () => {
  let component: RestaurantSetupComponent;
  let fixture: ComponentFixture<RestaurantSetupComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RestaurantSetupComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RestaurantSetupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
=======
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DishCardComponent } from './dish-card.component';

describe('DishCardComponent', () => {
  let component: DishCardComponent;
  let fixture: ComponentFixture<DishCardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DishCardComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DishCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
>>>>>>> master:client-server/src/app/components/dish-card/dish-card.component.spec.ts
