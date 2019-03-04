using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Engine : MonoBehaviour
{
    public static GameObject BaseGeom;
    PlanetSystem s1;

    // Use this for initialization
    void Start ()
    {
        Debug.Log("Started initialisation");
        BaseGeom = GameObject.CreatePrimitive(PrimitiveType.Sphere); // Creates a base geometry to clone from

        //########################################################################################################################

        s1 = new PlanetSystem(1.0f);
        s1.AddPlanet(1000.0f, new Vector3(0.0f, 0.0f, 0.0f), new Vector3(0.0f, 0.0f, 0.0f), true);
        s1.AddPlanet(1.0f, new Vector3(0.0f, 0.0f, 3.0f), new Vector3(30.0f, 30.0f, 0.0f), false);
        s1.AddPlanet(10.0f, new Vector3(0.0f, 0.0f, 4.4944f), new Vector3(50.0f, 0.0f, 0.0f), false);
        s1.AddPlanet(0.2f, new Vector3(0.0f, 0.0f, 6.0913f), new Vector3(54.0f, 0.0f, 0.0f), false);

        //########################################################################################################################

        BaseGeom.SetActive(false);                                   // Hides said base geometry, must be left until last
        Debug.Log("Booted");
    }

    // Update is called once per frame
    void FixedUpdate ()
    {
        s1.UpdateSystem();
	}
}




public class Planet // Class Describing a planet
{
    public float m;         // m mass kg
    public Vector3 v;       // v velocity vector {x,y,z} ms^-1
    public Vector3 u;       // u; position vector {x,y,x} m
    public bool isfixed;    // public bool isfixed; // true if planet is fixed i.e. the sun or free to move
    public float r;         // radius of planet
    public GameObject Geom; // Planets Geometry

    public Planet(float initm, Vector3 initv, Vector3 initu, bool initisfixed) // Initialiser for planet
    {
        m = initm;
        v = initv;
        u = initu;
        isfixed = initisfixed;
        r = (float)Math.Pow(m, 1.0f / 3.0f);                    // Makes radius proportional to mass
        Geom = UnityEngine.Object.Instantiate(Engine.BaseGeom); // Creates a clone of the base geometry
        Geom.transform.position = u;                            // Sets the position to the initial position
        Geom.transform.localScale = new Vector3(r, r, r);       // Scales Geometry to the radius
    }

    public void Move(Vector3 Deltau) // Simply moves the planet
    {
        u = u + Deltau;              // Updates u
        Geom.transform.position = u; // Updates the geometry position
    }
}




public class PlanetSystem // Class describing a whole system of planets
{
    public List<Planet> PlanetSystemList; // list of planets
    public float G; // gravitational constant

    public PlanetSystem(float Gravity)
        {
        PlanetSystemList = new List<Planet>(); // initiates the list holding the planet objects.
        G = Gravity;
        }

    public void AddPlanet(float initm, Vector3 initv, Vector3 initu, bool initisfixed)
    {
        //Planet TempPlanet = new Planet(initm, initv, initu, initisfixed);
        PlanetSystemList.Add(new Planet(initm, initv, initu, initisfixed));
        Debug.Log("added planet");
    }

    public Vector3 Attraction(Planet p1, Planet p2) // Calculates the acceleration on body 2 from body 1
    {
        var u = p2.u - p1.u;
        return -G * p1.m * u * (float)Math.Pow(u.magnitude, -3.0f);
    }

    public void UpdateSystem() // Updates the entire system over a given timestep.
    {
        foreach (var i in PlanetSystemList)
        {
            var suma = new Vector3( 0.0f, 0.0f, 0.0f ); 
            foreach (var j in PlanetSystemList)
            {
                if (i.u != j.u) suma += Attraction(j, i);
            }
            if (i.isfixed == false)
            {
                i.v = i.v + suma * Time.deltaTime;
                i.u = i.u + i.v * Time.deltaTime;
                i.Geom.transform.position = i.u;
            }
        }
    }
}