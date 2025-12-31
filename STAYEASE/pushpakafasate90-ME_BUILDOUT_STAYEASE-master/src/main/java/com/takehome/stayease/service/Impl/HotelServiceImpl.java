package com.takehome.stayease.service.Impl;

import lombok.RequiredArgsConstructor;
import java.util.List;
import com.takehome.stayease.dto.hotel.CreateHotelRequest;
import com.takehome.stayease.dto.hotel.UpdateHotelRequest;
import com.takehome.stayease.entity.Hotel;
import com.takehome.stayease.repository.HotelRepository;
import com.takehome.stayease.service.HotelService;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class HotelServiceImpl implements HotelService {

    private final HotelRepository hotelRepository;

    @Override
    public Hotel createHotel(CreateHotelRequest request) {
        Hotel hotel = Hotel.builder()
        .name(request.getName())
        .location(request.getLocation())
        .description(request.getDescription())
        .availableRooms(request.getAvailableRooms())
        .totalRooms(request.getAvailableRooms())
        .build();

        return hotelRepository.save(hotel);
    }

    @Override
    public List<Hotel> getAllHotels() {
        return hotelRepository.findAll();
    }

    @Override
    public Hotel updateHotel(Long hotelId, UpdateHotelRequest request) {

        Hotel hotel = hotelRepository.findById(hotelId)
                .orElseThrow(() -> new RuntimeException("Hotel not found"));

        if(request.getName() != null){
            hotel.setName(request.getName());
        }

        if(request.getLocation() != null){
            hotel.setLocation(request.getLocation());
        }

        if(request.getDescription() != null){
            hotel.setDescription(request.getDescription());
        }

        if(request.getAvailableRooms() != null){
            hotel.setAvailableRooms(request.getAvailableRooms());
        }

        return hotelRepository.save(hotel);
    }

    @Override
    public void deleteHotel(Long hotelId) {
        if(!hotelRepository.existsById(hotelId)){
            throw new RuntimeException("Hotel not found.");
        }
        hotelRepository.deleteById(hotelId);
    }

}
