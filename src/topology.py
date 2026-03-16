from src.geometry import simplify_polygon, find_space_containing_point

def find_emergency_door(door, signs):
    """
    Identify emergency exit doors based on the presence of nearby exit signs.
    """
    for sign in signs:
        # Check if the sign is close enough to the door (e.g., within 50 pixels)
        sign_x = (sign.bbox[0] + sign.bbox[2]) // 2
        sign_y = (sign.bbox[1] + sign.bbox[3]) // 2
        dx = sign_x - door.center[0]
        dy = sign_y - door.center[1]

        distance = (dx*dx + dy*dy)

        if distance < 50*50:
            door.is_emergency_exit = True
            return True
    return False

def find_spaces_door(door, spaces):
    """
    Assign spaces to a door based on location.
    """
    # Door geometry derived from detection output.
    cx, cy = door.center
    x1, y1, x2, y2 = door.bbox

    door_w = x2 - x1
    door_h = y2 - y1

    # Sample points offset from the door center to probe adjacent spaces.
    offset = max(12, int(min(door_w, door_h) * 2))

    # Orient the sample points along the door's normal direction.
    if abs(door.orientation_deg - 90.0) < 1e-6:
        point_a = (cx - offset, cy)
        point_b = (cx + offset, cy)
    else:
        point_a = (cx, cy - offset)
        point_b = (cx, cy + offset)

    # Look up which spaces contain the sample points.
    space_a = find_space_containing_point(point_a, spaces)
    space_b = find_space_containing_point(point_b, spaces)

    # Assign space ids for each side of the door.
    door.space_id_a = None if space_a is None else space_a.id
    door.space_id_b = None if space_b is None else space_b.id

    # Mark doors that connect an interior space to the exterior.
    door.is_external = (
        (door.space_id_a is None and door.space_id_b is not None) or
        (door.space_id_b is None and door.space_id_a is not None)
    )

def assign_spaces_to_doors(doors, spaces, signs):
    """
    Assign spaces to doors based on their location.
    """
    for door in doors:
        # Identify which spaces are adjacent to the door by sampling points on either side.
        find_spaces_door(door, spaces)

        # Identify emergency exit doors based on nearby signs.
        find_emergency_door(door, signs)
