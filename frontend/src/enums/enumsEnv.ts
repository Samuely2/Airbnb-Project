// Status de reserva
export enum ReservationStatus {
    PENDING = "pendente",
    CONFIRMED = "confirmada",
    CANCELED = "cancelada"
  }
  
  // Tipo de salão
  export enum HallType {
    APARTMENT = "APARTAMENT",
    HOUSE = "HOUSE",
    HOTEL = "HOTEL"
  }
  
  // Tipo de usuário
  export enum UserType {
    OWNER = 1,
    CONTRACTOR = 2,
    BOTH = 3
  }
  
  // Utilitários
  export const EnumUtils = {
    getReservationStatusLabel: (status: ReservationStatus): string => {
      switch (status) {
        case ReservationStatus.PENDING: return "Pendente";
        case ReservationStatus.CONFIRMED: return "Confirmada";
        case ReservationStatus.CANCELED: return "Cancelada";
        default: return String(status);
      }
    },
    
    getHallTypeLabel: (type: HallType): string => {
      switch (type) {
        case HallType.APARTMENT: return "Apartamento";
        case HallType.HOUSE: return "Casa";
        case HallType.HOTEL: return "Hotel";
        default: return String(type);
      }
    },
    
    getUserTypeLabel: (type: UserType): string => {
      switch (type) {
        case UserType.OWNER: return "Proprietário";
        case UserType.CONTRACTOR: return "Contratante";
        case UserType.BOTH: return "Proprietário e Contratante";
        default: return String(type);
      }
    }
  };