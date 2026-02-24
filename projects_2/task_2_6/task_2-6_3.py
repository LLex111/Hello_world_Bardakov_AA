donor = input("Группу крови донора (I, II, III, IV)")
recip = input("Группу крови реципиента (I, II, III, IV)")
if donor == "I":
    print("Можно")
elif recip == "IV":
    print("Можно")
elif recip == "I" and donor == "I":
    print("Можно")
elif recip == "II" and donor == "II":
    print("Можно")
elif recip == "III" and donor == "III":
    print("Можно")
else:
    print("Нельзя")

