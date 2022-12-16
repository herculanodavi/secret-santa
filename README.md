# secret-santa

An application that performs a Secret Santa shuffle that guarantees people that the giver knows the receiver, then sends an email to each participant informing their chosen person.

All information about the participants should be informed by a json with the following schema: 

```
[
    {
        "name": "Max Mustermann",
        "email": "max@mustermann.com",
        "pronoun": "ele",
        "groups": [
            "work",
            "coding",
            "brothers"
        ]
    },
    ...
]
```

Groups are clusters of people that know one another. The solution constraint is that all (giver, receiver) pairs have at least one group in common, and that the whole graph is a single cycle.
