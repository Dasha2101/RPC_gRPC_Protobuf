from protobuf import glossary_pb2

TERMS = {
    "Honeypot": glossary_pb2.Term(
        keyword="Honeypot",
        description="Система или ресурс, предназначенный для привлечения злоумышленников с целью наблюдения и анализа их действий."
    ),
    "Honeytoken": glossary_pb2.Term(
        keyword="Honeytoken",
        description="Ложные данные или объекты, которые используют для обнаружения несанкционированного доступа."
    ),
    "Deception Technology": glossary_pb2.Term(
        keyword="Deception Technology",
        description="Технологии обмана, используемые для создания фальшивых систем и ресурсов для отвлечения атакующих."
    ),
    "Low-Interaction Honeypot": glossary_pb2.Term(
        keyword="Low-Interaction Honeypot",
        description="Простейший тип honeypot, который имитирует ограниченное количество сервисов для сбора базовой информации о злоумышленниках."
    ),
    "High-Interaction Honeypot": glossary_pb2.Term(
        keyword="High-Interaction Honeypot",
        description="Сложный honeypot, который имитирует полноценную систему для глубокого анализа действий злоумышленников."
    ),
    "Attack Vector": glossary_pb2.Term(
        keyword="Attack Vector",
        description="Способ или путь, используемый злоумышленником для проникновения в систему."
    ),
    "Intrusion Detection": glossary_pb2.Term(
        keyword="Intrusion Detection",
        description="Процесс обнаружения попыток несанкционированного доступа к системе."
    ),
    "Logging": glossary_pb2.Term(
        keyword="Logging",
        description="Сбор и хранение информации о действиях злоумышленников для анализа и расследования."
    ),
    "Fake Service": glossary_pb2.Term(
        keyword="Fake Service",
        description="Ложный сервис, создаваемый в honeypot для заманивания атакующих."
    ),
}